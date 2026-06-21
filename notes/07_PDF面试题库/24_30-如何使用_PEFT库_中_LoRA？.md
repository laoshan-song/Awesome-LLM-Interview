# 30-如何使用 PEFT库 中 LoRA？

> 来源 PDF：`200页AI大模型面试高频必刷题（附详解）/30-如何使用 PEFT库 中 LoRA？.pdf`  
> 主题：Transformer / 基础架构  
> 页数：14  
> 字符数：16128  
> 索引片段数：40

## 摘要

如何使用 PEFT库 中 LoRA？ 来自： AiGC面试宝典 宁静致远 2024年01月28日 10:12 一、前言 本文章 主要介绍 使用 LoRA 对 大模型进行 高效参数微调，涉及内容： 涉及框架 • 如何使用 PEFT库 中 LoRA？ • 一、前言 • 二、如何 配置 LoraConfig？ • 三、模型 加入PEFT策略 • 3.1 模型加载 策略有哪些？ • 3.2 模型显存占用的部分有哪些？ • 3.3 模型显存占用 优化策略？ • 3.3.1 8bit量化 优化策略？ • 3.3.2 梯度检查 

## 代表性原文片段

### 片段 1

如何使用 PEFT库 中 LoRA？
来自： AiGC面试宝典
宁静致远 2024年01月28日 10:12
一、前言
本文章 主要介绍 使用 LoRA 对 大模型进行 高效参数微调，涉及内容：
涉及框架
• 如何使用 PEFT库 中 LoRA？
• 一、前言
• 二、如何 配置 LoraConfig？
• 三、模型 加入PEFT策略
• 3.1 模型加载 策略有哪些？
• 3.2 模型显存占用的部分有哪些？
• 3.3 模型显存占用 优化策略？
• 3.3.1 8bit量化 优化策略？
• 3.3.2 梯度检查 优化策略？
• 3.4 如何 向 模型 加入PEFT策略？
• 四、PEFT库 中 LoRA 模块 代码介绍
• 4.1 PEFT库 中 LoRA 模块 整体实现思路
• 4.2 PEFT库 中 LoRA 模块 _find_and_replace() 实现思路
• 4.3 PEFT库 中 Lora层的 实现思路
• 4.3.1 基类 LoraLayer 实现
• 4.3.2 Linear 实现
• 五、使用 LoRA 对 大模型进行 高效参数微调，如何进行存储？

### 片段 2

中 Lora层的 实现思路
• 4.3.1 基类 LoraLayer 实现
• 4.3.2 Linear 实现
• 五、使用 LoRA 对 大模型进行 高效参数微调，如何进行存储？
• 六、使用 LoRA 对 大模型进行 推理，如何进行加载？
• 七、huggingface大模型如何加载多个LoRA并随时切换？
• 参考
1. PEFT库 中 LoRA 模块使用；
2. PEFT库 中 LoRA 模块 代码介绍；
3. 在推理时如何先进行weight的合并在加载模型进行推理；
# 以下配置可能会随时间变化，出了问题就去issue里面刨吧
# 要相信你不是唯一一个大冤种！
accelerate
appdirs
loralib
bitsandbytes
black
black[jupyter]
datasets
fire
transformers>=4.28.0
扫码加
查看更多

-- 1 of 14 --

二、如何 配置 LoraConfig？
注意：target_modules中的作用目标名在不同模型中的名字是不一样的。query_key_value是在
ChatGLM中的名字
三、模型 加入PEFT策略

### 片段 3

Config？
注意：target_modules中的作用目标名在不同模型中的名字是不一样的。query_key_value是在
ChatGLM中的名字
三、模型 加入PEFT策略
3.1 模型加载 策略有哪些？
模型加载虽然很简单，这里涉及到2个时间换空间的大模型显存压缩技巧，主要说下load_in_8bit和
prepare_model_for_int8_training。
git+https://github.com/huggingface/peft.git
sentencepiece
gradio
wandb
cpm-kernel
# 设置超参数及配置
LORA_R = 8
LORA_ALPHA = 16
LORA_DROPOUT = 0.05
TARGET_MODULES = [
"q_proj",
"v_proj",
]
config = LoraConfig(
r=LORA_R,
lora_alpha=LORA_ALPHA,
target_modules=TARGET_MODULES,
lora_dropout=LORA_DROPOUT,
bias="none",
task_type="CAUSAL_LM",

### 片段 4

get_modules=TARGET_MODULES,
lora_dropout=LORA_DROPOUT,
bias="none",
task_type="CAUSAL_LM",
)
• 参数介绍：
• r：lora的秩，矩阵A和矩阵B相连接的宽度，r<<d；
• lora_alpha：归一化超参数，lora参数 ΔWx 被以 α/r 归一化，以便减少改变r rr时需要重新训练的计算
量；
• target_modules：lora的目标位置；
• merge_weights:eval模式中，是否将lora矩阵的值加到原有 W0 的值上;
• lora_dropout：lora层的dropout比率；
• fan_in_fan_out：只有应用在Conv1D层时置为True，其他情况False；
• bias: 是否可训练bias，none：均不可；all：均可；lora_only：只有lora部分的bias可训练；
• task_type：这是LoraConfig的父类PeftConfig中的参数，设定任务的类型；
• modules_to_save：除了lora部分之外，还有哪些层可以被训练，并且需要保存；

### 片段 5

pe：这是LoraConfig的父类PeftConfig中的参数，设定任务的类型；
• modules_to_save：除了lora部分之外，还有哪些层可以被训练，并且需要保存；

-- 2 of 14 --

3.2 模型显存占用的部分有哪些？
这里需要介绍一下 两个模型显存占用的部分：
3.3 模型显存占用 优化策略？
模型显存占用 有以下两种方式：
3.3.1 8bit量化 优化策略？
参考：https://huggingface.co/blog/hf-bitsandbytes-integration
from_pretrained中的load_in_8bit参数是bitsandbytes库赋予的能力，会把加载模型转化成混合8bit的量化模型，
注意这里的8bit模型量化只用于模型推理，通过量化optimizer state降低训练时显存的时8bit优化器是另一个功能
不要搞混哟~
模型量化本质是对浮点参数进行压缩的同时，降低压缩带来的误差。 8-bit quantization是把原始FP32（4字节）
压缩到Int8（1字节）也就是1/4的显存占用。如上加载后会发现除lora层外的多数层被转化成int类型如下

### 片段 6

误差。 8-bit quantization是把原始FP32（4字节）
压缩到Int8（1字节）也就是1/4的显存占用。如上加载后会发现除lora层外的多数层被转化成int类型如下
from peft import get_peft_model, LoraConfig, prepare_model_for_int8_training,
set_peft_model_state_dict
from transformers import AutoTokenizer, AutoModel
model = AutoModel.from_pretrained(
"THUDM/chatglm3-6b", load_in_8bit=True, torch_dtype=torch.float16,
trust_remote_code=True, device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(
"THUDM/chatglm3-6b", trust_remote_code=True
)

### 片段 7

)
tokenizer = AutoTokenizer.from_pretrained(
"THUDM/chatglm3-6b", trust_remote_code=True
)
model = prepare_model_for_int8_training(model)
1. 静态显存基本由模型参数量级决定；
2. 动态显存在向前传播的过程中每个样本的每个神经元都会计算激活值并存储，用于向后传播时的梯度计算，
这部分和batchsize以及参数量级相关；
1. 8bit量化优化。该方式只要用于优化 静态显存；
2. 梯度检查优化。该方式只要用于优化 动态显存；

-- 3 of 14 --

当然压缩方式肯定不是直接四舍五入，那样会带来巨大的精度压缩损失。常见的量化方案有absolute-maximum
和zero-point，它们的差异只是rescale的方式不同，这里简单说下absmax，如下
先寻找tensor矩阵的绝对值的最大值，并计算最大值到127的缩放因子，然后使用该缩放因子对整个tensor进行缩
放后，再round到整数。这样就把浮点数映射到了INT8,逆向回到float的原理相同。

### 片段 8

绝对值的最大值，并计算最大值到127的缩放因子，然后使用该缩放因子对整个tensor进行缩
放后，再round到整数。这样就把浮点数映射到了INT8,逆向回到float的原理相同。
当然以上的缩放方案依旧存在精度损失，以及当矩阵中存在outlier时，这个精度损失会被放大，例如当tensor中
绝大部分取值在1以下，有几个值在100+，则缩放后，所有1以下的tensor信息都会被round抹去。因此LLM.int8()
的实现对outlier做了进一步的优化，把outlier和非outlier的矩阵分开计算，再把结果进行合并来降低outlier对精度
的影响

-- 4 of 14 --

prepare_model_for_int8_training是对在Lora微调中使用LLM.int8()进行了适配用来提高训练的稳定性，主要包括
3.3.2 梯度检查 优化策略？
参考：https://medium.com/tensorflow/fitting-larger-networks-into-memory-583e3c758ff9

### 片段 9

检查 优化策略？
参考：https://medium.com/tensorflow/fitting-larger-networks-into-memory-583e3c758ff9
prepare_model_for_int8_training函数还做了一件事就是设置gradient_checkpointing=True，这是另一个时间换
空间的技巧。
gradient checkpoint的实现是在向前传播的过程中使用torch.no_grad()不去存储中间激活值，降低动态显存的占
用。而只是保存输入和激活函数，当进行反向传播的时候，会重新获取输入和激活函数计算激活值用于梯度计
算。因此向前传播会计算两遍，所以需要更多的训练时间。
3.4 如何 向 模型 加入PEFT策略？
其实lora微调的代码本身并不复杂，相反是如何加速大模型训练，降低显存占用的一些技巧大家可能不太熟悉。
模型初始化代码如下，get_peft_model会初始化PeftModel把原模型作为base模型，并在各个self-attention层加
入lora层，同时改写模型forward的计算方式。

### 片段 10

如下，get_peft_model会初始化PeftModel把原模型作为base模型，并在各个self-attention层加
入lora层，同时改写模型forward的计算方式。
注：use_cache设置为False，是因为和gradient checkpoint存在冲突。因为use_cache是对解码
速度的优化，在解码器解码时，存储每一步输出的hidden-state用于下一步的输入，而因为开启
了gradient checkpoint，中间激活值不会存储，因此use_cahe=False。其实#21737已经加入了
参数检查，这里设置只是为了不输出warning。
四、PEFT库 中 LoRA 模块 代码介绍
4.1 PEFT库 中 LoRA 模块 整体实现思路
具体 PEFT 包装 包装，结合PEFT模块的源码，来看一下LORA是如何实现的。
在PEFT模块中，peft_model.py中的PeftModel类是一个总控类，用于模型的读取保存等功能，继承了
transformers中的Mixin类，我们主要来看LORA的实现：
• layer norm层保留FP32精度

### 片段 11

eftModel类是一个总控类，用于模型的读取保存等功能，继承了
transformers中的Mixin类，我们主要来看LORA的实现：
• layer norm层保留FP32精度
• 输出层保留FP32精度保证解码时随机sample的差异性
# 加入PEFT策略
model = get_peft_model(model, config)
model = model.to(device)
model.config.use_cache = False

-- 5 of 14 --

代码位置：https://github.com/huggingface/peft/blob/main/src/peft/tuners/lora.py
从构造方法可以看出，这个类在创建的时候主要做了两步：
4.2 PEFT库 中 LoRA 模块 _find_and_replace() 实现思路
_find_and_replace() 实现思路：
注：其中这个replace的方法并不复杂，就是把原来的weight和bias赋给新创建的module，然后再分配到指定的设
备上：
class LoraModel(torch.nn.Module):

### 片段 12

lace的方法并不复杂，就是把原来的weight和bias赋给新创建的module，然后再分配到指定的设
备上：
class LoraModel(torch.nn.Module):
def __init__(self, config, model):
super().__init__()
self.peft_config = config
self.model = model
self._find_and_replace()
mark_only_lora_as_trainable(self.model, self.peft_config.bias)
self.forward = self.model.forward
• 第一步：self._find_and_replace()。找到所有需要加入lora策略的层，例如q_proj，把它们替换成lora模式；
• 第二步：mark_only_lora_as_trainable(self.model, self.peft_config.bias)。保留lora部分的参数可训练，其余
参数全都固定下来不动；
1. 找到需要的做lora的层：

## 使用建议

- 这些内容来自授权公开 PDF 的文本抽取结果，网页端会基于同一份静态索引做关键词检索。
- 面试复习时建议先用网页 PDF 原文检索定位题目，再回到主 notes 学系统化答案。
- 如果片段出现排版噪声，以原 PDF 语义为准，并优先整理成自己的回答模板。
