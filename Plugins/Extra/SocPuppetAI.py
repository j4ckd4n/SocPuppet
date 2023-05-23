from Plugins import Plugin

import gpt4all, os, sys

class SocPuppetAI(Plugin.Plugin):
  def __init__(self, question: str = None, name: str = "SocPuppetAI"):
    super().__init__(name)
    self._question: str = question
    
    self._env_path = os.getenv("AI_MODEL_PATH")
    if self._env_path is not None:
      self._root_path, self._file_name = os.path.split(self._env_path)
      self._gpt = gpt4all.GPT4All(self._file_name, self._root_path, 'llama')
    else:
      print("Model not specified, downloading ggml-wizardLM-7B.q4_2")
      self._gpt = gpt4all.GPT4All("ggml-wizardLM-7B.q4_2")
    self._system_prompt = {"role":"system", "content": "You are an assitant to a SOC (Security Operations Center) Analyst. Your job is to assist with findings, summarize details and provide suggestions for questions asked."}
    self._context_memory = [self._system_prompt]

  def run(self):
    while(True):
      if self._question == None:
        temp = ""
        inputs = []
        while not temp.lower().endswith('eof'):
          temp = str(input("> "))
          if "eof" in temp.lower():
            temp = temp.lower()
          inputs.append(temp)
        self._question = "\n".join(inputs)
        self._question.replace("eof", "")

      if self._question.startswith("clear_context"):
        self._context_memory.clear()
        self._context_memory.append(self._system_prompt)
        self._question = None
        continue
      elif self._question.startswith("exit_gpt"):
        self._context_memory.clear()
        return
      elif self._question.startswith("show_context"):
        print(self._context_memory)
        self._question = None
        continue
      
      self._context_memory.append({"role": "user", "content": self._question})
      res = self._gpt.chat_completion(self._context_memory, False, False, False)
      self._context_memory.append(res['choices'][0]["message"])
      print("SocPuppetAI: {}".format(res['choices'][0]["message"]["content"]))

      self._question = None
