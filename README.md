# Re_A
## 托管一些实践过程中使用/优化到的自用脚本
 - All_RepairDex.py为批量修复dex文件，主要是将脱壳后产生的多个dex文件，即计算dex的signature和checksum并回填至原dex文件中。
 - Hook_Sign.js为hook一些Java层中与签名校验有关的关键方法（待补充完善）并打印堆栈信息，用于检测并辅助定位签名校验的位置。
