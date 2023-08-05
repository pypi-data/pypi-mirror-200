import datetime
import hashlib
import os
import shutil
import sys
import glob
import sys

import numpy as np
import pandas as pd

import torch
import torch.nn as nn
from torch.optim import SGD, Adam
from torch.utils.data import DataLoader
import torch.optim.lr_scheduler as lr_scheduler

import pyro
import pyro.distributions as dist
from pyro.infer.autoguide import AutoDiagonalNormal
from pyro.infer import (
    SVI,
    Trace_ELBO,
    Predictive
)
from pyro.optim import ClippedAdam
import torch.nn.functional as F

from .utils import StockDataset, normalize
import pandas as pd
import matplotlib.pyplot as plt

from tqdm.auto import tqdm, trange
from dataclasses import dataclass

@dataclass
class ModelArgs:
    dropout: float = 0.1
    pretrained: bool = False
    lr: float = 0.001
    betas: tuple = (0.9, 0.999)
    lrd: float = 0.99996
    clip_norm: float = 10.0
    weight_decay: float = 0.001
    eps: float = 1e-8
    amsgrad: bool = False
    optim_args: float = 0.01
    gamma: float = 0.1
    step_size: float = 50

class ModelTrainer():

    def __init__(self, 
                 model = None,
                 **kwargs
                 ):
        for key, value in kwargs.items():
            setattr(ModelArgs, key, value)

        self.use_cuda = torch.cuda.is_available()
        self._initModel(model)

    def _modelEval(self):
        print(self._model.eval)
    
    def _initOptimizer(self):
        """
        Initializes the optimizer used to train the model.

        Returns:
            optimizer (torch.optim.AdamW): Optimizer instance
        """
        if self.type == "probabilistic":
            adam_params = {"lr": ModelArgs.lr, 
                            "betas": ModelArgs.betas,
                            "lrd": ModelArgs.lrd,
                            "weight_decay": ModelArgs.weight_decay
                        }
            return ClippedAdam(adam_params)
        elif self.type == "neural_network":
            return torch.optim.Adam(self._model.parameters(), 
                                    lr=ModelArgs.lr, 
                                    betas=ModelArgs.betas, 
                                    eps=ModelArgs.eps, 
                                    weight_decay=ModelArgs.weight_decay, 
                                    amsgrad=False)
        else:
            raise ValueError("Model type not recognized")
        
    def _initSVI(self):
        """
        Initializes a Stochastic Variational Inference (SVI) instance to optimize the model and guide.

        Returns:
            svi (pyro.infer.svi.SVI): SVI instance
        """
        if self._model.__class__.__name__[1:] == 'BayesianNN':
            return SVI(self._model, 
                    self._guide, 
                    self._initOptimizer(), 
                    loss=Trace_ELBO()
                    )
        else: 
            return SVI(self._model.model, 
                    self._guide, 
                    self._initOptimizer(), 
                    loss=Trace_ELBO()
                    )
        
    def _initScheduler(self):
        """
        Initializes a learning rate scheduler to control the learning rate during training.

        Returns:
            scheduler (pyro.optim.ExponentialLR): Learning rate scheduler
        """
        if self.type == "probabilistic":
            return pyro.optim.ExponentialLR({'optimizer': self._optimizer, 
                                            'optim_args': {'lr': ModelArgs.optim_args}, 
                                            'gamma': ModelArgs.gamma}
                                            )
        elif self.type == "neural_network":
            return torch.optim.lr_scheduler.StepLR(self._optimizer, 
                                                step_size=ModelArgs.step_size, 
                                                gamma=ModelArgs.gamma
                                                )
        else:
            raise ValueError("Model type not recognized")
        
    def _initTrainDl(self, 
                     x_train, 
                     batch_size, 
                     num_workers, 
                     sequence_length
                     ):
        """
        Initializes the training data loader.

        Parameters:
            x_train (numpy.ndarray or pandas dataset): the training dataset
            batch_size (int): the batch size to use for training
            num_workers (int): the number of workers to use for data loading
            sequence_length (int): the length of the input sequence

        Returns:
            train_dl (torch.utils.data.DataLoader): the training data loader
        """

        train_dl = StockDataset(x_train, sequence_length=sequence_length)

        train_dl = DataLoader(train_dl, 
                            batch_size=batch_size * (torch.cuda.device_count() \
                                                                   if self.use_cuda else 1),  
                            num_workers=num_workers,
                            pin_memory=self.use_cuda,
                            shuffle=True
                            )

        self._batch_size = batch_size
        self._num_workers = num_workers
        self._sequence_length = sequence_length

        return train_dl

    def _initValDl(self, 
                   x_test
                   ):
        """
        Initializes the validation data loader.

        Parameters:
            x_test (numpy.ndarray or pandas dataset): the validation dataset

        Returns:
            val_dl (torch.utils.data.DataLoader): the validation data loader
        """

        val_dl = StockDataset(x_test, 
                                sequence_length=self._sequence_length
                                )

        val_dl = DataLoader(val_dl, 
                            batch_size=self._batch_size * (torch.cuda.device_count() \
                                                    if self.use_cuda else 1), 
                            num_workers=self._num_workers,
                            pin_memory=self.use_cuda,
                            shuffle=False
                            )
        
        return val_dl
    
    def _initTrainValData(self, 
                          x_train,
                          validation_sequence,
                          batch_size,
                          num_workers,
                          sequence_length
                          ):
        """
        Initializes the training and validation data loaders.

        Parameters:
            x_train (numpy.ndarray): the training dataset
            validation_sequence (int): the number of time steps to reserve for validation during training
            batch_size (int): the batch size to use during training
            num_workers (int): the number of workers to use for data loading
            sequence_length (int): the length of the input sequence

        Returns:
            train_dl (torch.utils.data.DataLoader): the training data loader
            val_dl (torch.utils.data.DataLoader): the validation data loader
        """

        scaler = normalize(x_train)

        x_train = scaler.fit_transform()
        val_dl = x_train[-validation_sequence:]
        x_train = x_train[:len(x_train)-len(val_dl)]

        train_dl = self._initTrainDl(x_train, 
                                        batch_size=batch_size,
                                        num_workers=num_workers,
                                        sequence_length=sequence_length
                                        )

        val_dl = self._initValDl(val_dl)

        return train_dl, val_dl

    def fit(self, 
            x_train,
            epochs=10,
            sequence_length=30,
            batch_size=8, 
            num_workers=4,
            validation_sequence=30, 
            validation_cadence=5,
            patience=5
            ):
        """
        Fits the neural network model to a given dataset.

        Parameters:
            x_train (numpy.ndarray): the training dataset
            epochs (int): the number of epochs to train the model for
            sequence_length (int): the length of the input sequence
            batch_size (int): the batch size to use during training
            num_workers (int): the number of workers to use for data loading
            validation_sequence (int): the number of time steps to reserve for validation during training
            validation_cadence (int): how often to run validation during training
            patience (int): how many epochs to wait for improvement in validation loss before stopping early

        Returns:
            None
        """
        if self._model.__class__.__name__[1:] == 'MLP': sequence_length = 0
        if self._model.__class__.__name__[1:] == 'BayesianNN': sequence_length = 0

        train_dl, val_dl = self._initTrainValData(x_train,
                                                  validation_sequence,
                                                  batch_size,
                                                  num_workers,
                                                  sequence_length
                                                  )
        
        self._train(epochs,
                    train_dl,
                    val_dl,
                    validation_cadence,
                    patience
                    )
                
    def _train(self,
               epochs,
               train_dl,
               val_dl,
               validation_cadence,
               patience
               ):
        
        if self._model.__class__.__name__[1:] != 'GaussianHMM': 
            self._model.train()

        if self._model.__class__.__name__[1:] == 'DeepMarkovModel':
            self._model.rnn.train()

        best_loss = float('inf')
        counter = 0

        for epoch_ndx in tqdm((range(1, epochs + 1)), position=0, leave=True):
            epoch_loss = 0.0
            for x_batch, y_batch in train_dl:   
                if self.type == "neural_network":
                    self._optimizer.zero_grad()  
                    loss = self._computeBatchLoss(x_batch, y_batch)

                    loss.backward()     
                    self._optimizer.step()
                    epoch_loss += loss

                elif self.type == 'probabilistic':
                    loss = self._computeBatchLoss(x_batch, y_batch)
                    epoch_loss += loss

            self._scheduler.step()

            if epoch_ndx % validation_cadence != 0:                
                tqdm.write(f"Epoch {epoch_ndx}, Loss: {epoch_loss / len(train_dl)}", 
                           end='\r')

            else:
                val_loss = self._doValidation(val_dl)

                tqdm.write(f"Epoch {epoch_ndx}, Val Loss {val_loss}",
                           end='\r')

                # Early stopping
                stop, best_loss, counter = self._earlyStopping(val_loss, 
                                                               best_loss, 
                                                               counter, 
                                                               patience,
                                                               epoch_ndx
                                                               )
                if stop:
                    break   

    def _computeBatchLoss(self, 
                         x_batch, 
                         y_batch
                         ):     
        """
        Computes the loss for a given batch of data.

        Parameters:
            x_batch (torch.Tensor): the input data
            y_batch (torch.Tensor): the target data

        Returns:
            torch.Tensor: the loss for the given batch of data
        """  
        if self.type == "probabilistic":
            loss = self._svi.step(
                x_data=x_batch,
                y_data=y_batch
            )
        elif self.type == "neural_network":
            output = self._model(x_batch)
            loss_function = nn.MSELoss()
            loss = loss_function(output, y_batch)
        else:
            raise ValueError("Model type not recognized")
        
        return loss
    
    def _doValidation(self, val_dl):
        """
        Performs validation on a given validation data loader.

        Parameters:
            val_dl (torch.utils.data.DataLoader): the validation data loader

        Returns:
            float: the total loss over the validation set
        """

        val_loss = 0.0
        if self._model.__class__.__name__[1:] != 'GaussianHMM': 
            self._model.eval()
        with torch.no_grad():  
            for x_batch, y_batch in val_dl:
                if self.type == 'neural_network':
                    output = self._model(x_batch)
                    loss_fn = nn.MSELoss()
                    loss = loss_fn(output, y_batch)
                    val_loss += loss.item()
                elif self.type == 'probabilistic':
                    loss = self._svi.evaluate_loss(x_batch, y_batch)
                    val_loss += loss               

        return val_loss / len(val_dl)

    def _earlyStopping(self,
                       total_loss,
                       best_loss,
                       counter,
                       patience,
                       epoch_ndx
                       ):
        """
        Implements early stopping during training.

        Parameters:
            total_loss (float): the total validation loss
            best_loss (float): the best validation loss seen so far
            counter (int): the number of epochs without improvement in validation loss
            patience (int): how many epochs to wait for improvement in validation loss before stopping early
            epoch_ndx (int): the current epoch number

        Returns:
            tuple: a tuple containing a bool indicating whether to stop early, the best loss seen so far, and the current counter value
        """

        if total_loss < best_loss:
            best_loss = total_loss
            best_epoch_ndx = epoch_ndx
            self._saveModel(self._model.__class__.__name__[1:], 
                            best_epoch_ndx)
            counter = 0
        else:
            counter += 1

        if counter >= patience:
            print(f"No improvement after {patience} epochs. Stopping early.")
            return True, best_loss, counter
        else:
            return False, best_loss, counter
        
    def predict(self, 
                x_test
                ):
        """
        Make predictions on a given test set.

        Parameters:
            x_test (np.ndarray): the test set to make predictions on

        Returns:
            np.ndarray: the predicted values for the given test set
        """

        scaler = normalize(x_test)
        x_test = scaler.fit_transform()
        val_dl = self._initValDl(x_test)

        if self.type == "probabilistic":
            output = self._predict_probabilistic(val_dl)
        elif self.type == "neural_network":
            output = self._predict_neural_network(val_dl)
        else:
            raise ValueError("Model type not recognized")

        output = output.detach().numpy() * scaler.std() + scaler.mean()
                    
        return output
    
    def _predict_neural_network(self, 
                                val_dl):
        output = torch.tensor([])
        self._model.eval()
        
        with torch.no_grad():
            for x_batch, _ in val_dl:
                y_star = self._model(x_batch)
                output = torch.cat((output, y_star), 0)
                
        return output
    
    def _predict_probabilistic(self,
                               val_dl):
        
        if self._model.__class__.__name__[1:] == 'BayesianNN':
            output = torch.tensor([])
            for x_batch, _ in val_dl:
                predictive = Predictive(model=self._model, 
                                        guide=self._guide, 
                                        num_samples=self._batch_size,
                                        return_sites=("linear.weight", 
                                                        "obs", 
                                                        "_RETURN")
                                                    )
                samples = predictive(x_batch)
                site_stats = {}
                for k, v in samples.items():
                    site_stats[k] = {
                        "mean": torch.mean(v, 0)
                    }

                y_pred = site_stats['_RETURN']['mean']
                output = torch.cat((output, y_pred), 0)
            
            return output
        
        else: 
            # create a list to hold the predicted y values
            output = []

            # iterate over the test data in batches
            for x_batch, _ in val_dl:
                # make predictions for the current batch
                with torch.no_grad():
                    # compute the mean of the emission distribution for each time step
                    *_, z_loc, z_scale = self._guide(x_batch)
                    z_scale = F.softplus(z_scale)
                    z_t = dist.Normal(z_loc, z_scale).rsample()
                    mean_t, _ = self._model.emitter(z_t, x_batch)
                    
                    # get the mean for the last time step
                    mean_last = mean_t[:, -1, :]

                # add the predicted y values for the current batch to the list
                output.append(mean_last)

            # concatenate the predicted y values for all batches into a single tensor
            output = torch.cat(output)

            # reshape the tensor to get an array of shape [151,1]
            output = output.reshape(-1, 1)

            # return the predicted y values as a numpy array
            return output

    def _initModel(self, model):
        """
        Initializes the neural network model.

        Returns:
            None
        """
        
        if ModelArgs.pretrained:
            path = self._initModelPath(model, model.__class__.__name__[1:])
            model_dict = torch.load(path)
            model.load_state_dict(model_dict['model_state'])

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        if self.use_cuda:
            if torch.cuda.device_count() > 1:
                model = nn.DataParallel(model)
            self._model = model.to(device)

        self._model = model

        if self._model.model_type == "neural_network":
            self.type = 'neural_network'
        elif self._model.model_type == "probabilistic":
            self.type = 'probabilistic'
            if self._model.__class__.__name__[1:] == 'BayesianNN':
                self._guide = AutoDiagonalNormal(self._model)
            else:
                self._guide = self._model.guide
        
        pyro.clear_param_store()
        self._optimizer = self._initOptimizer()
        if self._model.model_type == "probabilistic":
            self._svi = self._initSVI()
        self._scheduler = self._initScheduler()

    def _saveModel(self, type_str, epoch_ndx):
        """
        Saves the model to disk.

        Parameters:
            type_str (str): a string indicating the type of model
            epoch_ndx (int): the epoch index

        Returns:
            None
        """

        file_path = os.path.join(
            '..', 
            '..', 
            'models', 
            self._model.__class__.__name__[1:], 
            type_str + '_{}_{}.state'.format(ModelArgs.dropout,
                                                ModelArgs.weight_decay
                                                ),
            )

        os.makedirs(os.path.dirname(file_path), mode=0o755, exist_ok=True)

        model = self._model
        if isinstance(model, torch.nn.DataParallel):
            model = model.module

        if self.type == 'neural_network':
            state = {
                'model_state': model.state_dict(),
                'model_name': type(model).__name__,
                'optimizer_state': self._optimizer.state_dict(),
                'optimizer_name': type(self._optimizer).__name__,
                'epoch': epoch_ndx
            }
        elif self.type == 'probabilistic':
            state = {
                'model_state': model.state_dict(),
                'model_name': type(model).__name__,
                'optimizer_state': self._optimizer.get_state(),
                'optimizer_name': type(self._optimizer).__name__,
                'epoch': epoch_ndx
            }         

        torch.save(state, file_path)

        with open(file_path, 'rb') as f:
            hashlib.sha1(f.read()).hexdigest()

    def _initModelPath(self, model, type_str):
        """
        Initializes the model path.

        Parameters:
            type_str (str): a string indicating the type of model

        Returns:
            str: the path to the initialized model
        """

        model_dir = '../../models/' + model.__class__.__name__[1:]
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        local_path = os.path.join(
            '..', 
            '..', 
            'models', 
            model.__class__.__name__[1:], 
            type_str + '_{}_{}.state'.format(ModelArgs.dropout,
                                                ModelArgs.weight_decay
                                                ),
            )

        file_list = glob.glob(local_path)
        
        if not file_list:
            raise ValueError(f"No matching model found in {local_path} for the given parameters.")
        
        # Return the most recent matching file
        return file_list[0]
    
    def trading(self, 
                predicted, 
                real, 
                shares=0, 
                stop_loss=0.0, 
                initial_balance=10000, 
                threshold=0.0, 
                plot=True
                ):


        """
        Simulate trading based on predicted and real stock prices.

        Args:
            predicted (np.ndarray): Array of predicted stock prices.
            real (np.ndarray): Array of real stock prices.
            shares (int): Number of shares held at the start of the simulation. Default is 0.
            stop_loss (float): Stop loss percentage. If the stock price falls below this percentage of the initial price,
                            all shares will be sold. Default is 0.0.
            initial_balance (float): Initial balance to start trading with. Default is 10000.
            threshold (float): Buy/Sell threshold. Default is 0.0.
            plot (bool): Whether to plot the trading simulation or not. Default is True.

        Returns:
            tuple: A tuple containing balance (float), total profit/loss (float), percentage increase (float), 
            and transactions (list of tuples). The transactions are of the form (timestamp, price, action, shares, balance).
        """
        
        assert predicted.shape == real.shape, "predicted and real must have the same shape"
        assert shares >= 0, "shares cannot be negative"
        assert initial_balance >= 0, "initial_balance cannot be negative"
        assert 0 <= stop_loss <= 1, "stop_loss must be between 0 and 1"

        transactions = []
        balance = initial_balance
        num_shares = shares
        total_profit_loss = 0

        if num_shares == 0 and balance >= real[0]:
            num_shares = int(balance / real[0])
            balance -= num_shares * real[0]
            transactions.append((0, real[0], "BUY", num_shares, balance))

        for i in range(1, len(predicted)):
            if predicted[i] > real[i-1] * (1 + threshold):
                if num_shares == 0:
                    num_shares = int(balance / real[i])
                    balance -= num_shares * real[i]
                    transactions.append((i, real[i], "BUY", num_shares, balance))
                elif num_shares > 0:
                    balance += num_shares * real[i]
                    total_profit_loss += (real[i] - real[i-1]) * num_shares
                    transactions.append((i, real[i], "SELL", num_shares, balance))
                    num_shares = 0
            elif predicted[i] < real[i-1] * (1 - threshold):
                if num_shares == 0:
                    continue
                elif num_shares > 0:
                    balance += num_shares * real[i]
                    total_profit_loss += (real[i] - real[i-1]) * num_shares
                    transactions.append((i, real[i], "SELL", num_shares, balance))
                    num_shares = 0

            if stop_loss > 0 and num_shares > 0 and real[i] < (real[0] - stop_loss):
                balance += num_shares * real[i]
                total_profit_loss += (real[i] - real[i-1]) * num_shares
                transactions.append((i, real[i], "SELL", num_shares, balance))
                num_shares = 0

        if num_shares > 0:
            balance += num_shares * real[-1]
            total_profit_loss += (real[-1] - real[-2]) * num_shares





            assert predicted.shape == real.shape, "predicted and real must have the same shape"
            assert shares >= 0, "shares cannot be negative"
            assert initial_balance >= 0, "initial_balance cannot be negative"
            assert 0 <= stop_loss <= 1, "stop_loss must be between 0 and 1"

            transactions = []
            balance = initial_balance
            num_shares = shares
            total_profit_loss = 0

            if num_shares == 0 and balance >= real[0]:
                num_shares = int(balance / real[0])
                balance -= num_shares * real[0]
                transactions.append((0, real[0], "BUY", num_shares, balance))

            for i in range(1, len(predicted)):
                if predicted[i] > real[i-1] * (1 + threshold):
                    if num_shares == 0:
                        num_shares = int(balance / real[i])
                        balance -= num_shares * real[i]
                        transactions.append((i, real[i], "BUY", num_shares, balance))
                    elif num_shares > 0:
                        balance += num_shares * real[i]
                        total_profit_loss += (real[i] - real[i-1]) * num_shares
                        transactions.append((i, real[i], "SELL", num_shares, balance))
                        num_shares = 0
                elif predicted[i] < real[i-1] * (1 - threshold):
                    if num_shares == 0:
                        continue
                    elif num_shares > 0:
                        balance += num_shares * real[i]
                        total_profit_loss += (real[i] - real[i-1]) * num_shares
                        transactions.append((i, real[i], "SELL", num_shares, balance))
                        num_shares = 0

                if stop_loss > 0 and num_shares > 0 and real[i] < (real[0] - stop_loss):
                    balance += num_shares * real[i]
                    total_profit_loss += (real[i] - real[i-1]) * num_shares
                    transactions.append((i, real[i], "SELL", num_shares, balance))
                    num_shares = 0

            if num_shares > 0:
                balance += num_shares * real[-1]
                total_profit_loss += (real[-1] - real[-2]) * num_shares
                transactions.append((len(predicted)-1, real[-1], "SELL", num_shares, balance))
                num_shares = 0

            percentage_increase = (balance - initial_balance) / initial_balance * 100

            if plot:
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(real, label='Real')
                ax.plot(predicted, label='Predicted')
                buy_scatter = ax.scatter([], [], c='g', marker='^', s=100)
                sell_scatter = ax.scatter([], [], c='r', marker='v', s=100)
                for transaction in transactions:
                    timestamp, price, action, shares, balance = transaction
                    if action == 'BUY':
                        buy_scatter = ax.scatter(timestamp, predicted[timestamp], c='g', marker='^', s=100)
                    elif action == 'SELL':
                        sell_scatter = ax.scatter(timestamp, predicted[timestamp], c='r', marker='v', s=100)
                ax.set_xlabel('Time')
                ax.set_ylabel('Price')
                ax.set_title('Trading Simulation')
                fig.autofmt_xdate()
                ax.legend((ax.plot([], label='Real')[0], ax.plot([], label='Predicted')[0], buy_scatter, sell_scatter),
                        ('Real', 'Predicted', 'Buy', 'Sell'))
                ax.text(0.05, 0.05, 
                        'Percentage increase: ${:.2f}%'.format(percentage_increase[0]), 
                        ha='left', va='center',
                        transform=ax.transAxes, 
                        bbox=dict(facecolor='white', alpha=0.5)
                        )
                plt.show()
            
            return balance, total_profit_loss, percentage_increase, transactions