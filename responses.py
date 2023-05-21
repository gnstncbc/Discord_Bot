def handle_response(message) -> str:
    p_message = message.lower()

    # if p_message == 'hello':
    #     return "Hey there!"
    
    # if p_message == 'eyv':
    #     return "Hadi eyv 👋🏻"
    
    # if p_message == 'emrah gey mi':
    #     return "evet"
    
    # if p_message == 'ilayın iqsu kaç':
    #     return "3"

    onemli_kisiler = ["berivan"]

    if any(word in p_message for word in onemli_kisiler):
        p_message = "onemli_kisiler_flag"
    
    match p_message:
        case "hello":
            return "Hey there!"
        case "eyv":
            return "Hadi eyv 👋🏻"
        case "emrah gey mi":
            return "evet"
        case "onemli_kisiler_flag":
            return "önemli birinden bahsediyorsun."
        case _:
            return "bilmiyommmm"