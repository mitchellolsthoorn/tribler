from Tribler.community.market.core.order import OrderId, OrderNumber, Order
from message import TraderId, MessageNumber, MessageId, Message
from price import Price
from quantity import Quantity
from timeout import Timeout
from timestamp import Timestamp


class Tick(Message):
    """Abstract class for representing a tick."""

    def __init__(self, message_id, order_id, price, quantity, timeout, timestamp, is_ask):
        """
        Initialise the tick

        Don't use this class directly

        :param message_id: A message id to identify the tick
        :param order_id: A order id to identify the order this tick represents
        :param price: A price to indicate for which amount to sell or buy
        :param quantity: A quantity to indicate how much to sell or buy
        :param timeout: A timeout when this tick is going to expire
        :param timestamp: A timestamp when the tick was created
        :param is_ask: A bool to indicate if this tick is an ask
        :type message_id: MessageId
        :type order_id: OrderId
        :type price: Price
        :type quantity: Quantity
        :type timeout: Timeout
        :type timestamp: Timestamp
        :type is_ask: bool
        """
        super(Tick, self).__init__(message_id, timestamp)

        assert isinstance(order_id, OrderId), type(order_id)
        assert isinstance(price, Price), type(price)
        assert isinstance(quantity, Quantity), type(quantity)
        assert isinstance(timeout, Timeout), type(timeout)
        assert isinstance(is_ask, bool), type(is_ask)

        self._order_id = order_id
        self._price = price
        self._quantity = quantity
        self._timeout = timeout
        self._is_ask = is_ask
        self._is_reserved = False

    @classmethod
    def from_order(cls, order, message_id):
        """
        Create a tick from an order

        :param order: The order that this tick represents
        :param message_id: The message id for the tick
        :return: The created tick
        :rtype: Tick
        """
        assert isinstance(order, Order), type(order)
        assert isinstance(message_id, MessageId), type(message_id)

        if order.is_ask():
            return Ask(message_id, order.order_id, order.price, order.total_quantity, order.timeout, order.timestamp)
        else:
            return Bid(message_id, order.order_id, order.price, order.total_quantity, order.timeout, order.timestamp)

    @property
    def order_id(self):
        """
        Return the order id of the tick

        :return: The order id
        :rtype: OrderId
        """
        return self._order_id

    @property
    def price(self):
        """
        Return the price of the tick

        :return: The price
        :rtype: Price
        """
        return self._price

    @property
    def quantity(self):
        """
        Return the quantity of the tick

        :return: The quantity
        :rtype: Quantity
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """
        Set the quantity of the tick

        :param quantity: The new quantity
        :type quantity: Quantity
        """
        assert isinstance(quantity, Quantity), type(quantity)
        self._quantity = quantity

    @property
    def timeout(self):
        """
        Return when the tick is going to expire

        :return: The timeout
        :rtype: Timeout
        """
        return self._timeout

    def is_ask(self):
        """
        Return if this tick is an ask

        :return: True if this tick is an ask, False otherwise
        :rtype: bool
        """
        return self._is_ask

    def is_reserved(self):
        """
        Return if this tick is reserved

        :return: True if this tick is reserved, False otherwise
        :rtype: bool
        """
        return self._is_ask

    def reserve(self):
        """
        Reserve this tick
        """
        self._is_reserved = True

    def release(self):
        """
        Release this tick
        """
        self._is_reserved = False

    def is_valid(self):
        """
        Return if the tick is still valid

        :return: True if valid, False otherwise
        :rtype: bool
        """
        return not (self._timeout.is_timed_out(Timestamp.now()) or self._is_reserved)

    def to_network(self):
        """
        Return network representation of the tick

        :return: tuple(<destination public identifiers>),tuple(<trader_id>, <message_number>, <price>, <quantity>, <timeout>, <timestamp>)
        :rtype: tuple, tuple
        """
        return tuple(), (
            str(self._order_id.trader_id),
            str(self._message_id.message_number),
            str(self._order_id.order_number),
            int(self._price),
            int(self._quantity),
            float(self._timeout),
            float(self._timestamp),
        )


class Ask(Tick):
    """Class representing an ask."""

    def __init__(self, message_id, order_id, price, quantity, timeout, timestamp):
        """
        Initialise the ask

        :param message_id: A message id to identify the ask
        :param order_id: A order id to identify the order this tick represents
        :param price: A price that needs to be paid for the ask
        :param quantity: The quantity that needs to be sold
        :param timeout: A timeout for the ask
        :param timestamp: A timestamp for when the ask was created
        :type message_id: MessageId
        :type order_id: OrderId
        :type price: Price
        :type quantity: Quantity
        :type timeout: Timeout
        :type timestamp: Timestamp
        """
        super(Ask, self).__init__(message_id, order_id, price, quantity, timeout, timestamp, True)

    @classmethod
    def from_network(cls, data):
        """
        Restore an ask from the network

        :param data: object with (trader_id, message_number, order_number, price, quantity, timeout, timestamp) properties
        :return: Restored ask
        :rtype: Ask
        """
        assert hasattr(data, 'trader_id')
        assert hasattr(data, 'message_number')
        assert hasattr(data, 'order_number')
        assert hasattr(data, 'price')
        assert hasattr(data, 'quantity')
        assert hasattr(data, 'timeout')
        assert hasattr(data, 'timestamp')

        return cls(
            MessageId(TraderId(data.trader_id), MessageNumber(data.message_number)),
            OrderId(TraderId(data.trader_id), OrderNumber(data.order_number)),
            Price.from_mil(data.price),
            Quantity(data.quantity),
            Timeout(data.timeout),
            Timestamp(data.timestamp),
        )


class Bid(Tick):
    """Class representing a bid."""

    def __init__(self, message_id, order_id, price, quantity, timeout, timestamp):
        """
        Initialise the bid

        :param message_id: A message id to identify the bid
        :param order_id: A order id to identify the order this tick represents
        :param price: A price that you are willing to pay for the bid
        :param quantity: The quantity that you want to buy
        :param timeout: A timeout for the bid
        :param timestamp: A timestamp for when the bid was created
        :type message_id: MessageId
        :type order_id: OrderId
        :type price: Price
        :type quantity: Quantity
        :type timeout: Timeout
        :type timestamp: Timestamp
        """
        super(Bid, self).__init__(message_id, order_id, price, quantity, timeout, timestamp, False)

    @classmethod
    def from_network(cls, data):
        """
        Restore a bid from the network

        :param data: object with (trader_id, message_number, order_number, price, quantity, timeout, timestamp) properties
        :return: Restored bid
        :rtype: Bid
        """
        assert hasattr(data, 'trader_id')
        assert hasattr(data, 'message_number')
        assert hasattr(data, 'order_number')
        assert hasattr(data, 'price')
        assert hasattr(data, 'quantity')
        assert hasattr(data, 'timeout')
        assert hasattr(data, 'timestamp')

        return cls(
            MessageId(TraderId(data.trader_id), MessageNumber(data.message_number)),
            OrderId(TraderId(data.trader_id), OrderNumber(data.order_number)),
            Price.from_mil(data.price),
            Quantity(data.quantity),
            Timeout(data.timeout),
            Timestamp(data.timestamp),
        )
