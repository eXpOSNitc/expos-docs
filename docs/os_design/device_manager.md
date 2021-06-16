---
title: 'Module 4: Device Manager'
original_url: 'http://eXpOSNitc.github.io/os_design-files/device_manager.html'
hide:
    - navigation
---

### `Dwrite(page#, block#)`

#### Arguments 
Memory page number, Disk block number 


#### Return Value

|  |  |
| --- | --- |
| 0 | Success |
| -1 | Failure |


#### Algorithm
```
Block for acquiring the disk.
Transfer contents of page number to disk block number.
Block for the transfer to complete.
Return success.
```


### `Dread(block#,page#)`

#### Arguments 
Disk block number, Memory page number 

#### Return Value

|  |  |
| --- | --- |
| 0 | Success |
| -1 | Failure |


#### Algorithm

```
Acquire the disk.
Transfer contents of disk block number to page number.
Block for the transfer to complete.
Return success.
```

### `Twrite(data)`

#### Arguments 
data 

#### Return Value

|  |  |
| --- | --- |
| 0 | Success |
| -1 | Failure |


#### Algorithm
```
Writes data into the terminal (non-blocking).
```


### `Tread(bufferptr)`

#### Arguments 
bufferptr 


#### Return Value

|  |  |
| --- | --- |
| 0 | Success |
| -1 | Failure |


#### Algorithm

```
Block for the terminal.
Read data and transfer to buffer.
```