import datetime
from ipaddress import ip_address

class ValueObject:
    def __init__(self, value=None):
        self.value = value
        self.is_writable = True
        self.is_changeable = True
        self.is_unique = False
    
    def get_value(self):
        return self.value

    def __eq__(self, other):
        if other is None:
            return False
        if not hasattr(other, 'value'):
            return False
        return self.value == other.value

    def __str__(self) -> str:
        return self.value


    def __repr__(self) -> str:
        return str(self.value)


class U(ValueObject):
    pass


class UInt(ValueObject):
    def __init__(self, value=None):
        if not isinstance(value, int):
            raise TypeError('Value should be int type')
        super().__init__(value)


class UFloat(ValueObject):
    def __init__(self, value=None):
        if not isinstance(value, float):
            raise TypeError('Value should be float type')
        super().__init__(value)


class UStr(ValueObject):
    def __init__(self, value=None):
        if not isinstance(value, str):
            raise TypeError(f'Value should be str type, but {type(value)} is given: {value}')
        super().__init__(value)


class UDict(ValueObject):
    def __init__(self, value=None):
        if not isinstance(value, dict):
            raise TypeError(f'Value should be dict type, but {type(value)} is given: {value}')
        super().__init__(value)


class UBool(ValueObject):
    def __init__(self, value=None):
        if not isinstance(value, bool):
            raise TypeError(f'Value should be bool type, but {type(value)} is given: {value}')
        super().__init__(value)


class UDate(ValueObject):
    def __init__(self, value=None):
        if value is None:
            value = datetime.datetime.utcnow()
        if not isinstance(value, datetime.datetime):
            raise ValueError(f'Value should be datetime type, but {type(value)} is given: {value}')
        super().__init__(value)

    def __str__(self) -> str:
        return self.value.replace(microsecond=0).isoformat()

    def __repr__(self) -> str:
        return self.value.replace(microsecond=0).isoformat()


class Status(UStr):
    def __init__(self, value='pending'):
        super().__init__(value)

    def is_pending(self):
        return self.value=='pending'

    def is_completed(self):
        return self.value in ['succeed', 'failed']

    def is_sent(self):
        return self.value=='sent'

    def is_running(self):
        return self.value=='running'

    def is_created(self):
        return self.value=='created'

    def is_creating(self):
        return self.value=='creating'

    def is_deploying(self):
        return self.value=='deploying'

    def is_deployed(self):
        return self.value=='deployed'

    def is_failed(self):
        return self.value=='failed'

    def is_processing(self):
        return self.value=='processing'

    def is_processed(self):
        return self.value=='processed'

    def is_succeed(self):
        return self.value=='succeed'

    def set_pending(self):
        self.value = 'pending'
        return self

    def set_sent(self):
        self.value = 'sent'
        return self

    def set_running(self):
        self.value = 'running'
        return self

    def set_creating(self):
        self.value = 'creating'
        return self

    def set_created(self):
        self.value = 'created'
        return self

    def set_deploying(self):
        self.value = 'deploying'
        return self

    def set_deployed(self):
        self.value = 'deployed'
        return self

    def set_failed(self):
        self.value = 'failed'
        return self

    def set_processing(self):
        self.value = 'processing'
        return self

    def set_processed(self):
        self.value = 'processed'
        return self

    def set_succeed(self):
        self.value = 'succeed'
        return self



class K3SNodeType(UStr):
    def __init__(self, value):
        super().__init__(value)

    def is_master(self):
        return self.value=='master'

    def match(self, value):
        return self.value==value


class IP(UStr):
    def __init__(self, value) -> None:
        if not self.is_ip(value):
            raise TypeError('Input parameter is not a ip')
        super().__init__(value)

    def is_private(self, ip)->bool:
        return ip_address(ip).is_private

    def is_ip(self, ip)->bool:
        try:
            ip_address(ip)
            return True
        except:
            return False
     