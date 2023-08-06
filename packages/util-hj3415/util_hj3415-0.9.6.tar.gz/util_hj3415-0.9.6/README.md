# util-hj3415

util-hj3415 is the collection of utility functions.

세가지 모듈이 존재한다. - krx, noti, utils

## Installation

[pip](https://pip.pypa.io/en/stable/) 를 사용하여 설치한다.

```bash
pip install util-hj3415
```

## Usage

### utils module
```python
from util_hj3415 import utils

def to_float(s) -> float:

def to_억(v) -> str:

def to_만(v) -> str:

def str_to_date(d: str) -> datetime.datetime:

def date_to_str(d: datetime.datetime) -> str:
```

### noti module
```python
from util_hj3415 import noti

def mail_to(title: str, text: str, mail_addr='hj3415@hanmail.net') -> bool:

BOT_LIST = ['manager', 'dart', 'eval']

def telegram_to(botname: str, text: str, parse_html: bool = False) -> bool:
```


### krx module
```python
from util_hj3415 import krx

MIN_REFRESH_DAY = 10

# krx 데이터베이스를 refresh 한다.
krx.make_db()

# 데이터베이스가 MIN_REFRESH_DAY 보다 오래되었는지 확인한다.
krx.is_old_krx()

# 전체 코드를 리스트로 반환한다.
krx.get_codes()

# 전체 코드를 키로하고 종목명을 값으로 하는 딕셔너리를 반환한다.
krx.get_name_codes()

# 삼성전자를 반환한다.
krx.get_name(code='005930')

# 전체 종목코드의 1/10을 날짜베이스로 반환한다.(dart 에서 사용한다.)
krx.get_parts()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)