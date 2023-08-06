#


## BasePolicyTrainer
[source](https://github.com/RLE-Foundation/Hsuanwu/blob/main/hsuanwu/common/engine/base_policy_trainer.py/#L16)
```python 
BasePolicyTrainer(
   train_env: Env, test_env: Env, cfgs: DictConfig
)
```


---
Base class of policy trainer.


**Args**

* **train_env**  : A Gym-like environment for training.
* **test_env**  : A Gym-like environment for testing.
* **cfgs**  : Dict config for configuring RL algorithms.


**Returns**

Base policy trainer instance.


**Methods:**


### .global_step
[source](https://github.com/RLE-Foundation/Hsuanwu/blob/main/hsuanwu/common/engine/base_policy_trainer.py/#L56)
```python
.global_step()
```

---
Get global training steps.


### .global_episode
[source](https://github.com/RLE-Foundation/Hsuanwu/blob/main/hsuanwu/common/engine/base_policy_trainer.py/#L62)
```python
.global_episode()
```

---
Get global training episodes.


### .train
[source](https://github.com/RLE-Foundation/Hsuanwu/blob/main/hsuanwu/common/engine/base_policy_trainer.py/#L152)
```python
.train()
```

---
Training function.


### .test
[source](https://github.com/RLE-Foundation/Hsuanwu/blob/main/hsuanwu/common/engine/base_policy_trainer.py/#L158)
```python
.test()
```

---
Testing function.

