def sim(str0, str1):
  """ Compare strings

  >>> sim("a b", "ab" )
  True
  >>> sim("a b", "a_b")
  True
  >>> sim("a b", "a-b")
  True
  >>> sim("ab" , "a_b")
  False
  >>> sim("ab" , "a-b")
  False
  >>> sim("a_b", "ab" )
  False
  >>> sim("a_b", "a-b")
  False
  >>> sim("a-b", "ab" )
  False
  >>> sim("a-b", "a_b")
  False
  """
  return str0 == str1.replace('-',' ').replace('_', ' ')