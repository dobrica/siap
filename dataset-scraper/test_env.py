import subprocess

print("\n")
print("Environment test: \n")
subprocess.call(['python', '--version'])
print("\n")
subprocess.call(['pip', '--version'])
print("\n")
subprocess.call(['pip','show','Scrapy'])