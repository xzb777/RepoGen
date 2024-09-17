import openai
import tiktoken
import sys
import os
from config import Config
import argparse
import time


class LLMUtil:
    OPENAI_API_KEY = Config.OPENAI_API_KEY
    GPT4_0125_PREVIEW_MODEL_NAME = "gpt-4-0125-preview"
    GPT4_1106_PREVIEW_MODEL_NAME = "gpt-4-1106-preview"
    GPT4_VISION_PREVIEW_MODEL_NAME = "gpt-4-vision-preview"
    GPT4_TURBO_PREVIEW_MODEL_NAME = "gpt-4-turbo-preview"
    GPT4_MODEL_NAME = "gpt-4"
    GPT4_32K_MODEL_NAME = "gpt-4-32k"
    GPT4_0613_MODEL_NAME = "gpt-4-0613"
    GPT4_32K_0613_MODEL_NAME = "gpt-4-32k-0613"
    GPT3_5_TURBO_0125_MODEL_NAME = "gpt-3.5-turbo-0125"
    GPT3_5_TURBO_1106_MODEL_NAME = "gpt-3.5-turbo-1106"
    GPT3_5_TURBO_MODEL_NAME = "gpt-3.5-turbo"
    GPT3_5_TURBO_16K_MODEL_NAME = "gpt-3.5-turbo-16k"
    GPT3_5_TURBO_INSTRUCT_MODEL_NAME = "gpt-3.5-turbo-instruct"
    Claude3_5_MODEL_NAME = "claude-3-5-sonnet-20240620"

    @staticmethod
    def ask_claude3_5(message, model=Claude3_5_MODEL_NAME, openai_key=OPENAI_API_KEY, temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            response_format={"type" : "json_object"},
            messages=message,
            temperature=temperature,
            max_tokens=8192,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            api_key=openai_key            )
        return response.choices[0]["message"]["content"]


    @staticmethod
    def get_tokens(prompt):
        prompt = str(prompt)
        embedding_encoding = Config.embedding_encoding
        encoding = tiktoken.get_encoding(embedding_encoding)
        tokens = encoding.encode(prompt, disallowed_special=())
        return tokens


    @staticmethod
    def get_top_k_tokens(prompt, k):
        embedding_encoding = Config.embedding_encoding
        encoding = tiktoken.get_encoding(embedding_encoding)
        tokens = encoding.encode(prompt, disallowed_special=())
        return tokens[:k]

    @staticmethod
    def calculate_token_nums_for_prompt(prompt):
        tokens = LLMUtil.get_tokens(prompt)

        return len(tokens)

    @staticmethod
    def ask_gpt3_5turbo(message, model=GPT3_5_TURBO_0125_MODEL_NAME, openai_key=OPENAI_API_KEY, temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            response_format={"type" : "json_object"},
            messages=message,
            temperature=temperature,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            api_key=openai_key            )
        return response.choices[0]["message"]["content"]


    @staticmethod
    def ask_gpt3_5turbo_json(message, model=GPT3_5_TURBO_0125_MODEL_NAME, openai_key=OPENAI_API_KEY, temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            response_format={"type" : "json_object"},
            messages=message,
            temperature=temperature,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            api_key=openai_key        
            )
        return response.choices[0]["message"]["content"]
    @staticmethod
    def ask_gpt3_5turbo16k(message, model=GPT3_5_TURBO_16K_MODEL_NAME, openai_key=OPENAI_API_KEY, temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            messages=message,
            temperature=temperature,
            max_tokens=12000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            api_key=openai_key        
            )
        return response.choices[0]["message"]["content"]

    @staticmethod
    def ask_gpt_4_preview(message, model=GPT4_0125_PREVIEW_MODEL_NAME, openai_key=OPENAI_API_KEY, temperature=0.2):
        response = openai.ChatCompletion.create(
            model=model,
            messages=message,
            response_format={"type" : "json_object"},
            temperature=temperature,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            api_key=openai_key
        )
        return response.choices[0]["message"]["content"]

    @staticmethod
    def ask_gpt4_turbo_preview(message, model=GPT4_TURBO_PREVIEW_MODEL_NAME, openai_key=OPENAI_API_KEY, temperature=0.2):
        response = openai.ChatCompletion.create(
            model=model,
            messages=message,
            response_format={"type" : "json_object"},
            temperature=temperature,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            api_key=openai_key
        )
        return response.choices[0]["message"]["content"]
    
    @staticmethod
    def ask_gpt4_1106_turbo_preview(message, model=GPT4_1106_PREVIEW_MODEL_NAME, openai_key=OPENAI_API_KEY, temperature=0.3):
        response = openai.ChatCompletion.create(
            model=model,
            messages=message,
            response_format={"type" : "json_object"},
            temperature=temperature,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            api_key=openai_key
        )
        return response.choices[0]["message"]["content"]


    @staticmethod
    def ask_gpt_4_32k(message, model=GPT4_32K_0613_MODEL_NAME, openai_key=OPENAI_API_KEY, temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            messages=message,
            temperature=temperature,
            max_tokens=8192,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            api_key=openai_key
        )
        return response.choices[0]["message"]["content"]

    @staticmethod
    def ask_o1_json(message, model="o1-preview", openai_key=OPENAI_API_KEY, temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            response_format={"type" : "json_object"},
            messages=message,
            temperature=temperature,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            api_key=openai_key        
            )
        return response.choices[0]["message"]["content"]






