from datasets import load_dataset
import pandas as pd

dataset = load_dataset("wikitablequestions")

item = dataset["test"][10] # show first test example

def to_pandas(item):
  return pd.DataFrame(item['table']["rows"],columns=item['table']["header"])

print(to_pandas(item))


from transformers import TapasConfig, TapasForQuestionAnswering

# for example, the base model finetuned on SQA
model = TapasForQuestionAnswering.from_pretrained("google/tapas-base")

# or, the base model finetuned on WTQ
# config = TapasConfig.from_pretrained("google/tapas-base-finetuned-wtq")
# model = TapasForQuestionAnswering.from_pretrained("google/tapas-base", config=config)

# or, the base model finetuned on WikiSQL
# config = TapasConfig("google-base-finetuned-wikisql-supervised")
# model = TapasForQuestionAnswering.from_pretrained("google/tapas-base", config=config)


from transformers import pipeline

tqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-wtq")




k_examples = 10
for item in dataset['test'].select(range(k_examples)):
  
  question = item['question']
  table = to_pandas(item)
  answer = tqa(table=table, query=question)['answer']

  print(table.to_markdown()) 
  print(f"Question: {question}")
  print(f"Predicted Answer: {answer}")
  print("Truth Answer: {0}".format(", ".join(item["answers"])))
  print("=============================================================================================\n")