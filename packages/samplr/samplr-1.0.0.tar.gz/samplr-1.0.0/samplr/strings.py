def header(
        func_name : str,
        count : int,
        output : int, 
        sample_type : str, 
        expand : bool, 
        info : bool
    ) -> str:
    return f'''\n\u001B[35m◆   ◇   ◆   ◇   ◆   ◇   ◆   ◇   ◆   ◇   ◆   \033[1m\033[3mS A M P L R\033[0m\u001B[35m   ◆   ◇   ◆   ◇   ◆   ◇   ◆   ◇   ◆   ◇   ◆\u001B[0m
\u001B[30m
◇ @samplr(count = {count}, sample_type = {sample_type}, expand = {expand}, info = {info})
  {func_name}()
◆ items returned: {count if count >=0 else len(output)+count} / {len(output)}
\u001B[0m'''

def footer() -> str:
    return '\n\u001B[35m◆   ◇   ◆   ◇   ◆   ◇   ◆   ◇   ◆   ◇   ◆     \033[3m E N D \u001B[0m\u001B[35m     ◆   ◇   ◆   ◇   ◆   ◇   ◆   ◇   ◆   ◇   ◆\u001B[0m'

def err_msg(err_code : int, *args : str) -> str:
    if err_code == 0:
        return '"count" must be of type int or equal "all".'
    elif err_code ==1:
        return f'"sample_type" must be one of {args[0]}.'
    elif err_code == 2:
        return '"info" must be of type bool.'
    elif err_code == 3:
        return '"expand" must be of type bool.'
    elif err_code == 4:
        return f'{args[0]} cannot de decorated with samplr as it does not return a list.'
    elif err_code == 5:
        return f'sample_type=random can not have a negative input count'