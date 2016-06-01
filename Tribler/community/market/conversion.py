from Tribler.Core.Utilities.encoding import encode, decode
from Tribler.dispersy.conversion import BinaryConversion
from Tribler.dispersy.message import DropPacket
from core.bitcoin_address import BitcoinAddress
from core.message import TraderId, MessageNumber
from core.order import OrderNumber
from core.price import Price
from core.quantity import Quantity
from core.timeout import Timeout
from core.timestamp import Timestamp
from core.transaction import TransactionNumber
from socket_address import SocketAddress
from ttl import Ttl


class MarketConversion(BinaryConversion):
    """Class that handles all encoding and decoding of Market messages."""

    def __init__(self, community):
        super(MarketConversion, self).__init__(community, "\x01")
        self.define_meta_message(chr(1), community.get_meta_message(u"ask"),
                                 self._encode_offer, self._decode_offer)
        self.define_meta_message(chr(2), community.get_meta_message(u"bid"),
                                 self._encode_offer, self._decode_offer)
        self.define_meta_message(chr(3), community.get_meta_message(u"proposed-trade"),
                                 self._encode_proposed_trade, self._decode_proposed_trade)
        self.define_meta_message(chr(4), community.get_meta_message(u"accepted-trade"),
                                 self._encode_accepted_trade, self._decode_accepted_trade)
        self.define_meta_message(chr(5), community.get_meta_message(u"declined-trade"),
                                 self._encode_declined_trade, self._decode_declined_trade)
        self.define_meta_message(chr(6), community.get_meta_message(u"counter-trade"),
                                 self._encode_proposed_trade, self._decode_proposed_trade)
        self.define_meta_message(chr(7), community.get_meta_message(u"start-transaction"),
                                 self._encode_start_transaction, self._decode_start_transaction)
        self.define_meta_message(chr(8), community.get_meta_message(u"multi-chain-payment"),
                                 self._encode_multi_chain_payment, self._decode_multi_chain_payment)
        self.define_meta_message(chr(9), community.get_meta_message(u"bitcoin-payment"),
                                 self._encode_bitcoin_payment, self._decode_bitcoin_payment)
        self.define_meta_message(chr(10), community.get_meta_message(u"end-transaction"),
                                 self._encode_end_transaction, self._decode_end_transaction)

    def _encode_offer(self, message):
        payload = message.payload
        packet = encode((
            str(payload.trader_id), str(payload.message_number), str(payload.order_number), int(payload.price),
            int(payload.quantity), float(payload.timeout), float(payload.timestamp), int(payload.ttl),
            str(payload.address.ip), int(payload.address.port)
        ))
        return packet,

    def _decode_offer(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the offer-payload")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid offer-payload type")

        if not len(payload) == 10:
            raise DropPacket("Invalid offer-payload length")

        trader_id, message_number, order_number, price, quantity, timeout, timestamp, ttl, ip, port = payload

        try:
            trader_id = TraderId(trader_id)
        except ValueError:
            raise DropPacket("Invalid 'trader_id' type")

        try:
            message_number = MessageNumber(message_number)
        except ValueError:
            raise DropPacket("Invalid 'message_number' type")

        try:
            order_number = OrderNumber(order_number)
        except ValueError:
            raise DropPacket("Invalid 'order_number' type")

        try:
            price = Price.from_mil(price)
        except ValueError:
            raise DropPacket("Invalid 'price' type")

        try:
            quantity = Quantity.from_mil(quantity)
        except ValueError:
            raise DropPacket("Invalid 'quantity' type")

        try:
            timeout = Timeout(timeout)
        except ValueError:
            raise DropPacket("Invalid 'timeout' type")

        try:
            timestamp = Timestamp(timestamp)
        except ValueError:
            raise DropPacket("Invalid 'timestamp' type")

        try:
            ttl = Ttl(ttl)
        except ValueError:
            raise DropPacket("Invalid 'ttl' type")

        try:
            address = SocketAddress(ip, port)
        except ValueError:
            raise DropPacket("Invalid 'address' type")

        return offset, placeholder.meta.payload.implement(trader_id, message_number, order_number, price, quantity,
                                                          timeout, timestamp, ttl, address)

    def _encode_proposed_trade(self, message):
        payload = message.payload
        packet = encode((
            str(payload.trader_id), str(payload.message_number), str(payload.order_number),
            str(payload.recipient_trader_id), str(payload.recipient_order_number), int(payload.price),
            int(payload.quantity), float(payload.timestamp)
        ))
        return packet,

    def _decode_proposed_trade(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the proposed-trade-payload")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid proposed-trade-payload type")

        if not len(payload) == 8:
            raise DropPacket("Invalid proposed-trade-payload length")

        trader_id, message_number, order_number, recipient_trader_id, recipient_order_number, price, quantity, timestamp = payload

        try:
            trader_id = TraderId(trader_id)
        except ValueError:
            raise DropPacket("Invalid 'trader_id' type")

        try:
            message_number = MessageNumber(message_number)
        except ValueError:
            raise DropPacket("Invalid 'message_number' type")

        try:
            order_number = OrderNumber(order_number)
        except ValueError:
            raise DropPacket("Invalid 'order_number' type")

        try:
            recipient_trader_id = TraderId(recipient_trader_id)
        except ValueError:
            raise DropPacket("Invalid 'recipient_trader_id' type")

        try:
            recipient_order_number = OrderNumber(recipient_order_number)
        except ValueError:
            raise DropPacket("Invalid 'recipient_order_number' type")

        try:
            price = Price.from_mil(price)
        except ValueError:
            raise DropPacket("Invalid 'price' type")

        try:
            quantity = Quantity.from_mil(quantity)
        except ValueError:
            raise DropPacket("Invalid 'quantity' type")

        try:
            timestamp = Timestamp(timestamp)
        except ValueError:
            raise DropPacket("Invalid 'timestamp' type")

        return offset, placeholder.meta.payload.implement(trader_id, message_number, order_number, recipient_trader_id,
                                                          recipient_order_number, price, quantity, timestamp)

    def _encode_accepted_trade(self, message):
        payload = message.payload
        packet = encode((
            str(payload.trader_id), str(payload.message_number), str(payload.order_number),
            str(payload.recipient_trader_id), str(payload.recipient_order_number), int(payload.price),
            int(payload.quantity), float(payload.timestamp), int(payload.ttl)
        ))
        return packet,

    def _decode_accepted_trade(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the accepted-trade-payload")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid accepted-trade-payload type")

        if not len(payload) == 9:
            raise DropPacket("Invalid accepted-trade-payload length")

        trader_id, message_number, order_number, recipient_trader_id, recipient_order_number, price, quantity, timestamp, ttl = payload

        try:
            trader_id = TraderId(trader_id)
        except ValueError:
            raise DropPacket("Invalid 'trader_id' type")

        try:
            message_number = MessageNumber(message_number)
        except ValueError:
            raise DropPacket("Invalid 'message_number' type")

        try:
            order_number = OrderNumber(order_number)
        except ValueError:
            raise DropPacket("Invalid 'order_number' type")

        try:
            recipient_trader_id = TraderId(recipient_trader_id)
        except ValueError:
            raise DropPacket("Invalid 'recipient_trader_id' type")

        try:
            recipient_order_number = OrderNumber(recipient_order_number)
        except ValueError:
            raise DropPacket("Invalid 'recipient_order_number' type")

        try:
            price = Price.from_mil(price)
        except ValueError:
            raise DropPacket("Invalid 'price' type")

        try:
            quantity = Quantity.from_mil(quantity)
        except ValueError:
            raise DropPacket("Invalid 'quantity' type")

        try:
            timestamp = Timestamp(timestamp)
        except ValueError:
            raise DropPacket("Invalid 'timestamp' type")

        try:
            ttl = Ttl(ttl)
        except ValueError:
            raise DropPacket("Invalid 'ttl' type")

        return offset, placeholder.meta.payload.implement(trader_id, message_number, order_number, recipient_trader_id,
                                                          recipient_order_number, price, quantity, timestamp, ttl)

    def _encode_declined_trade(self, message):
        payload = message.payload
        packet = encode((
            str(payload.trader_id), str(payload.message_number), str(payload.order_number),
            str(payload.recipient_trader_id), str(payload.recipient_order_number), float(payload.timestamp)
        ))
        return packet,

    def _decode_declined_trade(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the declined-trade-payload")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid declined-trade-payload type")

        if not len(payload) == 6:
            raise DropPacket("Invalid declined-trade-payload length")

        trader_id, message_number, order_number, recipient_trader_id, recipient_order_number, timestamp = payload

        try:
            trader_id = TraderId(trader_id)
        except ValueError:
            raise DropPacket("Invalid 'trader_id' type")

        try:
            message_number = MessageNumber(message_number)
        except ValueError:
            raise DropPacket("Invalid 'message_number' type")

        try:
            order_number = OrderNumber(order_number)
        except ValueError:
            raise DropPacket("Invalid 'order_number' type")

        try:
            recipient_trader_id = TraderId(recipient_trader_id)
        except ValueError:
            raise DropPacket("Invalid 'recipient_trader_id' type")

        try:
            recipient_order_number = OrderNumber(recipient_order_number)
        except ValueError:
            raise DropPacket("Invalid 'recipient_order_number' type")

        try:
            timestamp = Timestamp(timestamp)
        except ValueError:
            raise DropPacket("Invalid 'timestamp' type")

        return offset, placeholder.meta.payload.implement(trader_id, message_number, order_number, recipient_trader_id,
                                                          recipient_order_number, timestamp)

    def _encode_start_transaction(self, message):
        payload = message.payload
        packet = encode((
            str(payload.trader_id), str(payload.message_number), str(payload.transaction_number),
            float(payload.timestamp)
        ))
        return packet,

    def _decode_start_transaction(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the start_transaction")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid start_transaction type")

        if not len(payload) == 4:
            raise DropPacket("Invalid start_transaction length")

        trader_id, message_number, transaction_number, timestamp = payload

        try:
            trader_id = TraderId(trader_id)
        except ValueError:
            raise DropPacket("Invalid 'trader_id' type")

        try:
            message_number = MessageNumber(message_number)
        except ValueError:
            raise DropPacket("Invalid 'message_number' type")

        try:
            transaction_number = TransactionNumber(transaction_number)
        except ValueError:
            raise DropPacket("Invalid 'transaction_number' type")

        try:
            timestamp = Timestamp(timestamp)
        except ValueError:
            raise DropPacket("Invalid 'timestamp' type")

        return offset, placeholder.meta.payload.implement(trader_id, message_number, transaction_number, timestamp)

    def _encode_multi_chain_payment(self, message):
        payload = message.payload
        packet = encode((
            str(payload.trader_id), str(payload.message_number), str(payload.transaction_number),
            str(payload.bitcoin_address), int(payload.transferor_quantity), int(payload.transferee_quantity),
            float(payload.timestamp)
        ))
        return packet,

    def _decode_multi_chain_payment(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the multi_chain_payment")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid multi_chain_payment type")

        if not len(payload) == 7:
            raise DropPacket("Invalid multi_chain_payment length")

        trader_id, message_number, transaction_number, bitcoin_address, transferor_quantity, transferee_quantity,\
        timestamp = payload

        try:
            trader_id = TraderId(trader_id)
        except ValueError:
            raise DropPacket("Invalid 'trader_id' type")

        try:
            message_number = MessageNumber(message_number)
        except ValueError:
            raise DropPacket("Invalid 'message_number' type")

        try:
            transaction_number = TransactionNumber(transaction_number)
        except ValueError:
            raise DropPacket("Invalid 'transaction_number' type")

        try:
            bitcoin_address = BitcoinAddress(bitcoin_address)
        except ValueError:
            raise DropPacket("Invalid 'bitcoin_address' type")

        try:
            transferor_quantity = Quantity.from_mil(transferor_quantity)
        except ValueError:
            raise DropPacket("Invalid 'transferor_quantity' type")

        try:
            transferee_quantity = Quantity.from_mil(transferee_quantity)
        except ValueError:
            raise DropPacket("Invalid 'transferee_quantity' type")

        try:
            timestamp = Timestamp(timestamp)
        except ValueError:
            raise DropPacket("Invalid 'timestamp' type")

        return offset, placeholder.meta.payload.implement(trader_id, message_number, transaction_number,
                                                          bitcoin_address, transferor_quantity, transferee_quantity,
                                                          timestamp)

    def _encode_bitcoin_payment(self, message):
        payload = message.payload
        packet = encode((
            str(payload.trader_id), str(payload.message_number), str(payload.transaction_number), int(payload.quantity),
            float(payload.timestamp)
        ))
        return packet,

    def _decode_bitcoin_payment(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the bitcoin_payment")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid bitcoin_payment type")

        if not len(payload) == 5:
            raise DropPacket("Invalid bitcoin_payment length")

        trader_id, message_number, transaction_number, quantity, timestamp = payload

        try:
            trader_id = TraderId(trader_id)
        except ValueError:
            raise DropPacket("Invalid 'trader_id' type")

        try:
            message_number = MessageNumber(message_number)
        except ValueError:
            raise DropPacket("Invalid 'message_number' type")

        try:
            transaction_number = TransactionNumber(transaction_number)
        except ValueError:
            raise DropPacket("Invalid 'transaction_number' type")

        try:
            quantity = Quantity.from_mil(quantity)
        except ValueError:
            raise DropPacket("Invalid 'quantity' type")

        try:
            timestamp = Timestamp(timestamp)
        except ValueError:
            raise DropPacket("Invalid 'timestamp' type")

        return offset, placeholder.meta.payload.implement(trader_id, message_number, transaction_number, quantity,
                                                          timestamp)

    def _encode_end_transaction(self, message):
        payload = message.payload
        packet = encode((
            str(payload.trader_id), str(payload.message_number), str(payload.transaction_number),
            float(payload.timestamp)
        ))
        return packet,

    def _decode_end_transaction(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the end_transaction")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid end_transaction type")

        if not len(payload) == 4:
            raise DropPacket("Invalid end_transaction length")

        trader_id, message_number, transaction_number, timestamp = payload

        try:
            trader_id = TraderId(trader_id)
        except ValueError:
            raise DropPacket("Invalid 'trader_id' type")

        try:
            message_number = MessageNumber(message_number)
        except ValueError:
            raise DropPacket("Invalid 'message_number' type")

        try:
            transaction_number = TransactionNumber(transaction_number)
        except ValueError:
            raise DropPacket("Invalid 'transaction_number' type")

        try:
            timestamp = Timestamp(timestamp)
        except ValueError:
            raise DropPacket("Invalid 'timestamp' type")

        return offset, placeholder.meta.payload.implement(trader_id, message_number, transaction_number, timestamp)