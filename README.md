# airodor-wifi
provide a simple web application and api for the airodor wifi module from limot

To run this application:

```
flask --debug run
```

# Reverse Engineered API
General address to contact

```http://<ip-address>/msg&Function=<action><group><mode>```

```
action = [R, W, T, S] 
where:
  R = READ MODE 
  W = SET MODE 
  T = READ OFF-TIMER 
  S = SET OFF-TIMER 
```
 
```
group = [A, B, D, S, T] 

A = vent group A
B = vent group B
currently: D, S, T are unknown, where S, T might be the filter status
Three messages are therefor unknown:
RS0
RT0
RD68
```

```
mode: 
  ventilation modes:
    0 = Off 
    1 = min (alternating)
    2 = med (alternating)
    4 = max (alternating, when setting) 
    6 = max (alternating, when reading) 
    8 = med (permanent one direction)
    16 = max (permanent one direction)
    32 = med (permanent only to inside)
    64 = max (permanent only to inside)
```
```
  timer modes: (timers are only usable to turn the ventilation off, not for other modes)
    0 = off 
    1..12 = hours 
 ```
```
answers: 
  R -> value = R<group><mode> 
  W -> success = M<group>OK 
  T -> value = T<group><mode> 
  S -> success = S<group>OK 
```


  

