import yfinance as yf
import matplotlib.pyplot as plt

# Download the data
data1 = yf.download("^GSPC")['Close']
data2 = yf.download("^IXIC")['Close']
data3 = yf.download("GC=F")['Close']

# Plot the data
plt.figure(figsize=(14, 7))

#plt.plot(data1.index, data1, label='S&P 500 (^GSPC)', color='blue')
#plt.plot(data2.index, data2, label='NASDAQ (^IXIC)', color='green')
plt.plot(data3.index, data3, label='Gold (GC=F)', color='orange')

# Add titles and labels
plt.title('Closing Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()

# Show the plot
plt.show()
