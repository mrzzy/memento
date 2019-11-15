#
# Memento
# Backend 
# Messaging Broker
#

from abc import ABC, abstractmethod
from uuid import uuid4

# defines an abstract publish/subscribe message broker
class AbstractBroker(ABC):
    # subscribe to message sent on the given channel 
    # running the given callback when a message is sent on the channel
    # channel - name of the channel to subscribe to
    # callback - callback to run when recieving message, message passed to first argument
    # returns a subscribe_id that identifies the subscription
    @abstractmethod
    def subscribe(self, channel, callback):
        pass

    # unsubscribe from given channel 
    # channel - channel to unsubscribe from
    # subscribe_id - the id of subscription to unsubscribe from
    @abstractmethod
    def unsubscribe(self, subscribe_id):
        pass

    # publish the given message on the given channel
    # channel - name of the channel to publish the channel
    # message - string message to publish on the channel
    @abstractmethod
    def publish(self, channel, message):
        pass

    # clear the given notification channel
    # removes all subscribers on the channel
    # channel - name of the channel to clear
    @abstractmethod
    def clear(self, channel):
        pass

# defines a local message broker
class LocalBroker(AbstractBroker):
    def __init__(self):
        self.message_board = {}

    # subscribe to message sent on the given channel 
    # running the given callback when a message is sent on the channel
    # channel - name of the channel to subscribe to
    # callback - callback to run when recieving message, message passed to first argument
    # returns a subscribe_id that identifies the subscription
    def subscribe(self, channel, callback):
        # check if channel exists otherwise create one
        if not channel in self.message_board:
            self.message_board[channel] = {}
        # record callback for channel
        subscribe_id = uuid4()
        self.message_board[channel][subscribe_id] = callback

    # unsubscribe from given channel 
    # does not do anything if not already is subscribed to the channel
    # channel - channel to unsubscribe from
    # subscribe_id - the id of subscription to unsubscribe from
    def unsubscribe(self, channel, subscribe_id):
        if subscribe_id in self.message_board[channel]:
            del self.message_board[channel][subscribe_id]

    # publish the given message on the given channel
    # channel - name of the channel to publish the channel
    # message - string message to publish on the channel
    def publish(self, channel, message):
        # check if channel exists otherwise create one
        if not channel in self.message_board:
            self.message_board[channel] = {}

        # publish message by running registered callbacks
        for callback in self.message_board[channel].values():
            callback(message)

    # clear the given notification channel
    # removes all subscribers on the channel
    # channel - name of the channel to clear
    def clear(self, channel):
        for subscribe_id in self.message_board[channel].keys():
            self.unsubscribe(channel, subscribe_id)
