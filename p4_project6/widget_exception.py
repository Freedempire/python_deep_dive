from http import HTTPStatus
import json
from datetime import datetime, timezone
import traceback

class WidgetException(Exception):
    """Base exception for widget application"""
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_err_msg = 'widget exception occurred'
    user_err_msg = 'an unexpected internal error occurred'

    def __repr__(self):
        return f'{type(self).__name__}({self.http_status}, {self.internal_err_msg}, {self.user_err_msg})'

    def log_exception(self, file=None):
        if file is None:
            file = 'log.txt'
        with open(file, 'a+') as f:
            f.write(f'Exception: {datetime.now(timezone.utc)}, {self!r}\n')

            # traceback.print_exception(self, file=f)
            # add indentation to each line of traceback string
            f.writelines(map(lambda row: f'\n    {row[1:]}' if row.startswith('\n') else f'    {row}',
                             traceback.format_exception(self)))
            f.write('\n')

    def to_json(self):
        return json.dumps({
            'exception_type': type(self).__name__,
            'http_status': self.http_status,
            'internal_message': self.internal_err_msg,
            'user_message': self.user_err_msg
        })

class SupplierException(WidgetException):
    """General supplier-end exception"""
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_err_msg = 'supplier exception occurred'
    user_err_msg = 'an unexpected internal error occurred'

class NotManufacturedError(SupplierException):
    """Indicate an error due to manufacturing discontinuation"""
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_err_msg = 'exception caused by manufacturing discontinuation'
    user_err_msg = 'the widget requested is no longer manufactured by supplier'

class ProductionDelayedError(SupplierException):
    """Indicate an error due to production delay"""
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_err_msg = 'error caused by production delay'
    user_err_msg = 'production was delayed by supplier'

class ShippingDelayedError(SupplierException):
    """Indicate an error due to shipping delay"""
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_err_msg = 'error caused by shipping delay'
    user_err_msg = 'shipping was delayed by supplier'

class CheckoutException(WidgetException):
    """General checkout-end exception"""
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_err_msg = 'exception caused by checkout'
    user_err_msg = 'an unexpected internal error occurred'

class InventoryException(CheckoutException):
    """Indicates an exception relating to inventory"""
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_err_msg = 'exception caused by inventory'
    user_err_msg = 'an unexpected internal error occurred'

class OutOfStockError(InventoryException):
    """Indicates an error due to inventory defficiency"""
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_err_msg = 'error caused by stock insufficiency'
    user_err_msg = 'not enough stock for the widget requested'

class PricingException(CheckoutException):
    """Indicates an exception relating to pricing"""
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_err_msg = 'exception caused by pricing'
    user_err_msg = 'an unexpected internal error occurred'

class InvalidCouponCodeError(PricingException):
    """Indicates an error due to invalid coupon code"""
    http_status = HTTPStatus.BAD_REQUEST
    internal_err_msg = 'error caused by invalid coupon code'
    user_err_msg = 'the coupon code provided is invalid'

class NotStackableError(PricingException):
    """Indicates an error due to stacking unsupported coupons"""
    http_status = HTTPStatus.BAD_REQUEST
    internal_err_msg = 'error caused by stacking unsupported coupons'
    user_err_msg = 'the coupons provided cannot be stacked'

try:
    raise PricingException()
except PricingException:
    try:
        raise InvalidCouponCodeError()
    except InvalidCouponCodeError as ex:
        ex.log_exception()
        print(ex.to_json())

try:
    raise OutOfStockError()
except OutOfStockError as ex:
    ex.log_exception()
    print(ex.to_json())