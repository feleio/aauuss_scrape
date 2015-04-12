import os
import re

__all__ = [x[:-3] for x in os.listdir('scraper') if re.match(r'.+\.py$',x) and x != '__init__.py']
