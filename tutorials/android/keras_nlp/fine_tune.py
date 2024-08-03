start = time.time()

cnn_ds = tfds.load('cnn_dailymail', as_supervised=True)

end = time.time()
print("TOTAL TIME ELAPSED: ", end - start)


for article, highlights in cnn_ds['train']:
  print(article.numpy())
  print(highlights.numpy())
  break


from nltk import tokenize
import nltk

nltk.download('punkt')

def merge_sentences(sentences, max_length):
    res = []
    cur_len = 0
    cur_sentences = []
    for s in sentences:
        if cur_len + len(s) > max_length:
            # If adding the next sentence exceeds `max_length`, we add the
            # current sentences into collection
            res.append(" ".join(cur_sentences))
            cur_len = len(s)
            cur_sentences = [s]
        else:
            cur_len += len(s)
            cur_sentences.append(s)
    res.append(" ".join(cur_sentences))
    return res

import progressbar

max_length = 512
all_sentences = []
count = 0
total = len(cnn_ds["train"])
num_articles_to_process = 20000
progressbar_update_freq = 2000

widgets = [' [',
         progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
         '] ',
           progressbar.Bar('*'),' (',
           progressbar.ETA(), ') ',
          ]

# Render a progressbar to track progress
bar = progressbar.ProgressBar(
    max_value=num_articles_to_process // progressbar_update_freq + 2,
    widgets=widgets).start()

for article, highlight in cnn_ds['train']:
  # Use NLTK tokenize to split articles into sentences
  sentences = tokenize.sent_tokenize(str(article))
  # Merge individual sentences into longer context
  combined_res = merge_sentences(sentences, max_length)
  # Add merged context into collection
  all_sentences.extend(combined_res)
  count += 1
  if count % progressbar_update_freq == 0:
    bar.update(count / progressbar_update_freq)
  if count >= num_articles_to_process:
    break


tf_train_ds = tf.data.Dataset.from_tensor_slices(all_sentences)
processed_ds = tf_train_ds.map(gpt2_preprocessor, tf.data.AUTOTUNE).batch(20).cache().prefetch(tf.data.AUTOTUNE)
part_of_ds = processed_ds.take(100)


gpt2_lm.include_preprocessing = False

num_epochs = 1

lr = tf.keras.optimizers.schedules.PolynomialDecay(
    5e-5,
    decay_steps=part_of_ds.cardinality() * num_epochs,
    end_learning_rate=0.0,
)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
gpt2_lm.compile(
    optimizer=keras.optimizers.experimental.Adam(lr),
    loss=loss,
    weighted_metrics=["accuracy"])

gpt2_lm.fit(part_of_ds, epochs=num_epochs)


start = time.time()

output = gpt2_lm.generate("Breaking news: the river", max_length=200)
print("\nGPT-2 output:")
print(output.numpy().decode("utf-8"))

end = time.time()
print("TOTAL TIME ELAPSED: ", end - start)


gpt2_lm.backbone.save_weights("finetuned_model.h5")

del gpt2_tokenizer, gpt2_preprocessor, gpt2_lm


gpt2_lm = keras_nlp.models.GPT2CausalLM.from_preset("gpt2_base_en_cnn_dailymail")
# Alternative model: finetuned on Reddit dataset
# gpt2_lm = keras_nlp.models.GPT2CausalLM.from_preset("gpt2_base_en_reddit")
gpt2_lm.generate(
    ["Breaking news: the river"],
    max_length=200,
)