import json
import os
from typing import Any, Dict, List, Literal

import ctranslate2
import transformers


class M2M100(object):
    """Machine Translation Module.

    Args:
        model (Literal[&quot;m2m100_1.2b&quot;, &quot;m2m100_418m&quot;], optional): Model Options. Defaults to "m2m100_1.2b".
        device (Literal[&quot;cpu&quot;, &quot;cuda&quot;], optional): Device. Defaults to "cpu".
    """

    def __init__(
        self,
        model: Literal["m2m100_1.2b", "m2m100_418m"] = "m2m100_1.2b",
        device: Literal["cpu", "cuda"] = "cpu",
    ) -> None:
        HOME = os.path.expanduser("~")
        MODEL_DIR = "exciton/models/nlp/translation/m2m100"
        self.translator = ctranslate2.Translator(
            f"{HOME}/{MODEL_DIR}/{model}", device=device
        )
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            f"{HOME}/{MODEL_DIR}/{model}/tokenizer/"
        )
        with open(f"{HOME}/{MODEL_DIR}/support_languages.json") as fp:
            self.support_languages = json.load(fp)

    def get_support_languages(self) -> List[Dict[str, str]]:
        """Suppport Languages for M2M100

        Returns:
            List[Dict[str, str]]: List of languages supported by M2M100 models.
        """
        return [
            {"code": wd, "name": self.support_languages[wd]}
            for wd in self.support_languages
        ]

    def _batch(
        self, source: List[Dict[str, Any]], batch_size: int = 10
    ) -> List[List[Dict[str, Any]]]:
        """Create Batch.

        Args:
            source (List[Any]): Source List
            batch_size (int, optional): Batch Size. Defaults to 10.

        Returns:
            List[List[Any]]: Batches
        """
        output = []
        arr = []
        for k, itm in enumerate(source):
            itm["sent_id"] = k
            arr.append(itm)
            if len(arr) == batch_size:
                output.append(arr)
                arr = []
        if len(arr) > 0:
            output.append(arr)
        return output

    def predict(self, source: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Batch Translation.

        Args:
            source (List[Dict[str, Any]]): Source, input data.

        Returns:
            List[Dict[str, Any]]: Target, output data.

        Examples:
            >>> from exciton.nlp.translation import M2M100
            >>> model = M2M100(model="m2m100_418m", device="cuda")
            >>> source = [
                    {"source": "I love you!", "source_lang": "en", "target_lang": "zh"},
                    {"source": "我爱你！", "source_lang": "zh", "target_lang": "en"}
                ]
            >>> results = model.predict(source)
            >>> print(results)
        """
        output = []
        for batch in self._batch(source):
            print(batch)
            sen_list = []
            target_prefix = []
            for itm in batch:
                slang = itm["source_lang"]
                tlang = itm["target_lang"]
                if slang in self.support_languages and tlang in self.support_languages:
                    self.tokenizer.src_lang = slang
                    sen = self.tokenizer.encode(itm["source"])
                    sen = self.tokenizer.convert_ids_to_tokens(sen)
                    sen_list.append(sen)
                    target_prefix.append([self.tokenizer.lang_code_to_token[tlang]])
                else:
                    itm["target"] = None
                    output.append(itm)
            results = self.translator.translate_batch(
                sen_list,
                target_prefix=target_prefix,
                beam_size=3,
                no_repeat_ngram_size=2,
                repetition_penalty=1.2,
            )
            for k, out in enumerate(results):
                itm = batch[k]
                out = out.hypotheses[0][1:]
                out = self.tokenizer.decode(self.tokenizer.convert_tokens_to_ids(out))
                itm["target"] = out
                output.append(itm)
        output = sorted(output, key=lambda x: x["sent_id"])
        return output
