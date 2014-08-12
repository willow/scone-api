from src.libs.python_utils.collections.dict_utils import NoEmptyDict


def test_no_empty_dict_does_not_set_none():
  x = NoEmptyDict()
  x['test'] = 1
  x['foo'] = None
  assert len(x) == 1

def test_no_empty_dict_does_not_set_none_when_init():
  x = NoEmptyDict({'test':None})
  assert len(x) == 0


def test_no_empty_dict_does_not_set_none_when_update():
  x = NoEmptyDict()
  x.update({'test':None})
  assert len(x) == 0
