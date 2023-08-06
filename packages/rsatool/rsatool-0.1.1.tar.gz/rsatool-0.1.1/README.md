eng:
This module implements encryption using the RSA algorithm, as well as indirectly fast and reliable calculation of prime numbers
To generate keys, use the function RSA.get_bit_keys(number of bits to calculate the desired key)
```python
import RSA_tool
e, d, n = RSA_tool.RSA.get_bit_keys(256)
```
To encrypt information, use the block encryption function, you can quickly encrypt information of any size
```python
import RSA_tool
e, d, n = RSA_tool.RSA.get_bit_keys(256)
m = 'hello world'
print(n)
c = RSA_tool.RSA.block_encrypt(m, e, n)
print(c)
```
To decrypt the message, use the block decryption function
```python
import RSA_tool
e, d, n = RSA_tool.RSA.get_bit_keys(256)
m = 'hello world'
print(n)
c = RSA_tool.RSA.block_encrypt(m, e, n)
print(c)
m = RSA_tool.RSA.block_decrypt(c, d, n)
print(m)
```
For an example of working with the module and testing it, refer to the main.py file

rus:
Данный модуль реализует шифрование по алгоритму RSA, а так же косвенно быстрое и надёжное вычисление простых чисел
Для генерации ключей воспользуйтесь функцией RSA.get_bit_keys(число бит для вычисления желаемого ключа)
```python
import RSA_tool
e, d, n = RSA_tool.RSA.get_bit_keys(256)
```
Для шифрования информации используйте функцию блочного шифрования, Вы можете достаточно быстро шифровать информацию любого объёма
```python
import RSA_tool
e, d, n = RSA_tool.RSA.get_bit_keys(256)
m = 'hello world'
print(n)
c = RSA_tool.RSA.block_encrypt(m, e, n)
print(c)
```
Для расшифрования сообщения используйте фунцию блочного расшифрования
```python
import RSA_tool
e, d, n = RSA_tool.RSA.get_bit_keys(256)
m = 'hello world'
print(n)
c = RSA_tool.RSA.block_encrypt(m, e, n)
print(c)
m = RSA_tool.RSA.block_decrypt(c, d, n)
print(m)
```
Для примера работы с модулем и его тестирования обратитесь к файлу main.py
