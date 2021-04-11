class StdTx:
    def __init__(self, msg  , fee , signature , memo):
        self._msg = msg
        self._fee = fee
        self._signature = signature
        self._memo = memo

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg):
        self._msg = msg

    @property
    def fee(self):
        return self._fee

    @fee.setter
    def fee(self, fee):
        self._fee = fee

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, signature):
        self._signature = signature

    @property
    def memo(self):
        return self._memo

    @memo.setter
    def memo(self, memo):
        self._memo = memo