from datetime import datetime


class Util:
  @classmethod
  def current_time(self) -> datetime:
    now = datetime.now()
    formatted = now.strftime("%Y%m%d %H:%M:%S")
    return formatted
