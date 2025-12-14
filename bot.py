import os
import io
import zlib
import base64
import random
import string
import hashlib
import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents)

def generate_random_name(length=16):
    chars = string.ascii_letters + '_'
    return ''.join(random.choice(chars) for _ in range(length))

def xor_encrypt(data, key):
    result = bytearray()
    key_bytes = key.encode() if isinstance(key, str) else key
    for i, byte in enumerate(data):
        result.append(byte ^ key_bytes[i % len(key_bytes)])
    return bytes(result)

def lua_string_escape(s):
    escaped = s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    return f'"{escaped}"'

def obfuscate_lua(source_code):
    compressed = zlib.compress(source_code.encode('utf-8'), level=9)
    
    xor_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    encrypted = xor_encrypt(compressed, xor_key)
    
    encoded = base64.b64encode(encrypted).decode('ascii')
    
    vm_state = generate_random_name()
    vm_stack = generate_random_name()
    vm_pc = generate_random_name()
    vm_ops = generate_random_name()
    vm_exec = generate_random_name()
    decode_func = generate_random_name()
    decompress_func = generate_random_name()
    xor_func = generate_random_name()
    loader_func = generate_random_name()
    data_var = generate_random_name()
    key_var = generate_random_name()
    temp_var1 = generate_random_name()
    temp_var2 = generate_random_name()
    temp_var3 = generate_random_name()
    result_var = generate_random_name()
    byte_var = generate_random_name()
    idx_var = generate_random_name()
    chunk_var = generate_random_name()
    
    anti_debug_check = generate_random_name()
    integrity_check = generate_random_name()
    env_check = generate_random_name()
    
    checksum = hashlib.md5(source_code.encode()).hexdigest()[:16]
    
    obfuscated_parts = []
    
    obfuscated_parts.append(f"local {anti_debug_check}=function()")
    obfuscated_parts.append(f"if debug and debug.getinfo then return false end;")
    obfuscated_parts.append(f"if getfenv and getfenv(0)~=getfenv(1)then return false end;")
    obfuscated_parts.append(f"return true end;")
    
    obfuscated_parts.append(f"local {integrity_check}=function({temp_var1})")
    obfuscated_parts.append(f"local {temp_var2}=0;")
    obfuscated_parts.append(f"for {idx_var}=1,#{temp_var1}do {temp_var2}={temp_var2}+string.byte({temp_var1},{idx_var})end;")
    obfuscated_parts.append(f"return {temp_var2}%65536 end;")
    
    obfuscated_parts.append(f"local {env_check}=function()")
    obfuscated_parts.append(f"if not {anti_debug_check}()then error('Security violation detected')end;")
    obfuscated_parts.append(f"if _G.hook or _G.detour then error('Hook detected')end;")
    obfuscated_parts.append(f"return true end;")
    
    obfuscated_parts.append(f"{env_check}();")
    
    obfuscated_parts.append(f"local {xor_func}=function({data_var},{key_var})")
    obfuscated_parts.append(f"local {result_var}={{}};")
    obfuscated_parts.append(f"local {temp_var1}=#{key_var};")
    obfuscated_parts.append(f"for {idx_var}=1,#{data_var}do ")
    obfuscated_parts.append(f"local {byte_var}=string.byte({data_var},{idx_var});")
    obfuscated_parts.append(f"local {temp_var2}=string.byte({key_var},({idx_var}-1)%{temp_var1}+1);")
    obfuscated_parts.append(f"{result_var}[{idx_var}]=string.char(({byte_var}~{temp_var2})%256)end;")
    obfuscated_parts.append(f"return table.concat({result_var})end;")
    
    obfuscated_parts.append(f"local {decode_func}=function({data_var})")
    obfuscated_parts.append(f"local {temp_var1}='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';")
    obfuscated_parts.append(f"local {result_var}={{}};")
    obfuscated_parts.append(f"{data_var}=string.gsub({data_var},'[^'..{temp_var1}..'=]','');")
    obfuscated_parts.append(f"local {temp_var2}=string.gsub({data_var},'=','');")
    obfuscated_parts.append(f"for {chunk_var} in string.gmatch({temp_var2},'....?')do ")
    obfuscated_parts.append(f"local {temp_var3}=0;local {byte_var}=0;")
    obfuscated_parts.append(f"for {idx_var}=1,#{chunk_var}do ")
    obfuscated_parts.append(f"{temp_var3}={temp_var3}*64+(string.find({temp_var1},string.sub({chunk_var},{idx_var},{idx_var}))-1)end;")
    obfuscated_parts.append(f"for {idx_var}=1,#{chunk_var}-1 do ")
    obfuscated_parts.append(f"{byte_var}=#{chunk_var}-{idx_var};")
    obfuscated_parts.append(f"table.insert({result_var},string.char(({temp_var3}/2^({byte_var}*8))%256))end end;")
    obfuscated_parts.append(f"return table.concat({result_var})end;")
    
    obfuscated_parts.append(f"local {decompress_func}=function({data_var})")
    obfuscated_parts.append(f"local {temp_var1}=string.byte;local {temp_var2}=string.char;")
    obfuscated_parts.append(f"local {result_var}={{}};local {idx_var}=1;")
    obfuscated_parts.append(f"local {vm_pc}=1;local {temp_var3}=#{data_var};")
    obfuscated_parts.append(f"while {vm_pc}<={temp_var3} do ")
    obfuscated_parts.append(f"local {byte_var}={temp_var1}({data_var},{vm_pc});{vm_pc}={vm_pc}+1;")
    obfuscated_parts.append(f"if {byte_var}<128 then {result_var}[{idx_var}]={temp_var2}({byte_var});{idx_var}={idx_var}+1;")
    obfuscated_parts.append(f"else local {chunk_var}={byte_var}%32;")
    obfuscated_parts.append(f"local {vm_stack}=({byte_var}-{chunk_var})/32;")
    obfuscated_parts.append(f"if {vm_stack}==0 then {vm_stack}={temp_var1}({data_var},{vm_pc});{vm_pc}={vm_pc}+1 end;")
    obfuscated_parts.append(f"local {vm_ops}={temp_var1}({data_var},{vm_pc});{vm_pc}={vm_pc}+1;")
    obfuscated_parts.append(f"if {chunk_var}==0 then {chunk_var}={temp_var1}({data_var},{vm_pc});{vm_pc}={vm_pc}+1 end;")
    obfuscated_parts.append(f"{vm_ops}={vm_ops}*256+{chunk_var}+1;")
    obfuscated_parts.append(f"for {vm_state}={idx_var}-{vm_stack},{idx_var}-{vm_stack}+{vm_stack}-1 do ")
    obfuscated_parts.append(f"{result_var}[{idx_var}]={result_var}[{vm_state}];{idx_var}={idx_var}+1 end end end;")
    obfuscated_parts.append(f"return table.concat({result_var})end;")
    
    obfuscated_parts.append(f"local {vm_ops}={{")
    for i in range(8):
        op_name = generate_random_name(8)
        obfuscated_parts.append(f"[{i}]=function({vm_state})return {vm_state}+{random.randint(1,100)}end,")
    obfuscated_parts.append(f"}};")
    
    obfuscated_parts.append(f"local {vm_exec}=function({data_var})")
    obfuscated_parts.append(f"local {vm_pc}=0;")
    obfuscated_parts.append(f"for {idx_var}=1,#{data_var}do ")
    obfuscated_parts.append(f"{vm_pc}=({vm_pc}+string.byte({data_var},{idx_var}))%256 end;")
    obfuscated_parts.append(f"if {vm_pc}~=0 then return {data_var} end;")
    obfuscated_parts.append(f"return {data_var}end;")
    
    obfuscated_parts.append(f"local {loader_func}=function()")
    obfuscated_parts.append(f"if not {env_check}()then return end;")
    obfuscated_parts.append(f"local {data_var}={lua_string_escape(encoded)};")
    obfuscated_parts.append(f"local {key_var}={lua_string_escape(xor_key)};")
    obfuscated_parts.append(f"local {temp_var1}={decode_func}({data_var});")
    obfuscated_parts.append(f"if not {temp_var1}then error('Decode failed')end;")
    obfuscated_parts.append(f"local {temp_var2}={xor_func}({temp_var1},{key_var});")
    obfuscated_parts.append(f"if not {temp_var2}then error('Decrypt failed')end;")
    obfuscated_parts.append(f"local {temp_var3}={decompress_func}({temp_var2});")
    obfuscated_parts.append(f"if not {temp_var3}then error('Decompress failed')end;")
    obfuscated_parts.append(f"{temp_var3}={vm_exec}({temp_var3});")
    obfuscated_parts.append(f"local {result_var},err=loadstring({temp_var3});")
    obfuscated_parts.append(f"if not {result_var}then error('Load failed: '..(err or 'unknown'))end;")
    obfuscated_parts.append(f"return {result_var}()end;")
    
    obfuscated_parts.append(f"return {loader_func}()")
    
    obfuscated_code = ''.join(obfuscated_parts)
    
    return obfuscated_code

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    lua_code = None
    
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith('.lua') or attachment.filename.endswith('.txt'):
                try:
                    file_content = await attachment.read()
                    lua_code = file_content.decode('utf-8')
                    break
                except Exception as e:
                    await message.channel.send(f'Error reading file: {str(e)}')
                    return
    
    if not lua_code and message.content:
        content = message.content.strip()
        if content.startswith('```lua'):
            lua_code = content[6:-3] if content.endswith('```') else content[6:]
        elif content.startswith('```'):
            lua_code = content[3:-3] if content.endswith('```') else content[3:]
        elif 'function' in content or 'local' in content or 'return' in content:
            lua_code = content
    
    if lua_code:
        try:
            obfuscated = obfuscate_lua(lua_code)
            
            if len(obfuscated) < 1900:
                await message.channel.send(f'```lua\n{obfuscated}\n```')
            else:
                file_obj = io.BytesIO(obfuscated.encode('utf-8'))
                await message.channel.send(
                    'Obfuscated Lua code:',
                    file=nextcord.File(file_obj, filename='obfuscated.lua')
                )
        except Exception as e:
            await message.channel.send(f'Obfuscation error: {str(e)}')
    
    await bot.process_commands(message)

if __name__ == '__main__':
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print('Error: DISCORD_BOT_TOKEN environment variable not set')
        exit(1)
    bot.run(token)
