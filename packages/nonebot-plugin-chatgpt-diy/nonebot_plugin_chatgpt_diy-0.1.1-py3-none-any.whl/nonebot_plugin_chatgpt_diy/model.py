import openai


def get_chat_response(key, msg, start_sequence, bot_name, master_name) -> (str, bool):
    openai.api_key = key
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=msg,
            temperature=0.6,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[f" {bot_name}:", f" {master_name}:"]
        )
        res = response['choices'][0]['text'].strip()
        if start_sequence[1:] in res:
            res = res.split(start_sequence[1:])[1]
        return res, True
    except Exception as e:
        return f"发生错误: {e}", False


async def get_response(content, key):
    openai.api_key = key
    openai.proxy="http://127.0.0.1:7890"
    try:
        res_ = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=content
        )

    except Exception as error:
        print(error)
        return

    res = res_.choices[0].message.content
    while res.startswith("\n") != res.startswith("？"):
        res = res[1:]
    return res
