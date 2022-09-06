import sys
sys.stdout = sys.stderr = open('sai.out','w')

print('Saída')

import os
os.system('ping localhost')

sys.stdin.close()