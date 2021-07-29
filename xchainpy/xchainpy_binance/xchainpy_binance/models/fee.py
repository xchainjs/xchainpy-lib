class Fee:
    def __init__(self, msg_type:str, fee, fee_for:int):
        self._msg_type = msg_type
        self._fee = fee
        self._fee_for = fee_for

    @property
    def msg_type(self):
        return self._msg_type

    @msg_type.setter
    def msg_type(self, msg_type):
        self._msg_type = msg_type

    @property
    def fee(self):
        return self._fee

    @msg_type.setter
    def fee(self, fee):
        self._fee = fee

    @property
    def fee_for(self):
        return self._fee_for

    @fee_for.setter
    def fee_for(self, fee_for):
        self._fee_for = fee_for


class TransferFee:
    def __init__(self, fixed_fee_params:Fee, multi_transfer_fee:int, lower_limit_as_multi:int):
        self._fixed_fee_params = fixed_fee_params
        self._multi_transfer_fee = multi_transfer_fee
        self._lower_limit_as_multi = lower_limit_as_multi

    @classmethod
    def from_binance_fee(cls, transfer_fee):
        """Get TransferFee object from a binance fee

        :param transfer_fee: binance fee
        :type transfer_fee: dict
        :returns: TransferFee object
        """
        return TransferFee(fixed_fee_params=Fee(msg_type=transfer_fee['fixed_fee_params']['msg_type'],
                                                fee=transfer_fee['fixed_fee_params']['fee'],
                                                fee_for=transfer_fee['fixed_fee_params']['fee_for']),
                            multi_transfer_fee=transfer_fee['multi_transfer_fee'],
                            lower_limit_as_multi=transfer_fee['lower_limit_as_multi'])
    
    @property
    def fixed_fee_params(self):
        return self._fixed_fee_params

    @fixed_fee_params.setter
    def fixed_fee_params(self, fixed_fee_params):
        self._fixed_fee_params = fixed_fee_params

    @property
    def multi_transfer_fee(self):
        return self._multi_transfer_fee

    @multi_transfer_fee.setter
    def multi_transfer_fee(self, multi_transfer_fee):
        self._multi_transfer_fee = multi_transfer_fee

    @property
    def lower_limit_as_multi(self):
        return self._lower_limit_as_multi

    @lower_limit_as_multi.setter
    def lower_limit_as_multi(self, lower_limit_as_multi):
        self._lower_limit_as_multi = lower_limit_as_multi