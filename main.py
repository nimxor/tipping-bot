import click
import discord
import os
from discord.ext import commands
import store
import wallet
import error
import re

BISON_DIGITS = 1
BISON_REPR = "BISON TOKEN"

bot_description = f"Tip {BISON_REPR} to other users on your server."
bot_help_register = "Register or change your deposit address."
bot_help_info = "Get your account's info."
bot_help_withdraw = f"Withdraw {BISON_REPR} from your balance."
bot_help_balance = f"Check your {BISON_REPR} balance."
bot_help_tip = f"Give {BISON_REPR} to a user from your balance."

bot = commands.Bot(command_prefix='$')
regex = r'addr([0-9]+([a-zA-Z]+[0-9]+)+)'
patter = re.compile(regex)
max_length = 200


@bot.event
async def on_ready():
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)


@bot.command()
async def test(ctx):
    await ctx.send('I heard you! {0}'.format(ctx.author))


@bot.command(pass_context=True)
async def command(ctx):
    await ctx.send(
        '**$info**: See your address.\n'
        '**$register <wallet_address>**: Register a wallet to your account. You cannot register more then one wallet\n'
        '**$balance**: See your current balance.\n'
        '**$tip <user_mention> <amount>**: Tip <amount> BISON to <user_mention>.\n'
        '**$withdraw <amount>**: LOL you can\'t withdraw. \n'
    )


@bot.command(pass_context=True, help=bot_help_info)
async def info(ctx):
    print("************************INFO***************************")
    user = store.register_user(ctx.author.id)
    if user.actual_address.address is None:
        await ctx.send("Please register your address using $register")
    else:
        await ctx.send("Your address is *{0}*".format(user.actual_address.address))


@bot.command(pass_context=True, help=bot_help_register)
async def register_other(ctx, member: discord.Member, wallet_address: str):
    author_id = ctx.author.id
    print("************************REGISTER OTHER***************************")
    print(author_id)
    print(wallet_address)
    if not (author_id == 968207994070368306 or author_id == 807103891182845992):
        await ctx.send("Only Admin can perform this operation!")
        return

    if not (patter.match(wallet_address) and len(wallet_address) <= max_length):
        await ctx.send("Please use proper address!")
        return

    user_id = member.id
    print(user_id)
    user_wallet = wallet.getWallet(user_id)
    print(user_wallet)
    if user_wallet is not None:
        print("Hello World!")
        existing_user = store.register_user(user_id)
        prev_address = existing_user.actual_address.address
        new_user = store.register_user(user_id, wallet_address)
        if prev_address:
            print_user_db(user_id)
            await ctx.send(
                f'You changed {member.mention} address from:\n'
                f'`{prev_address}`\n to\n '
                f'`{new_user.actual_address.address}`')
            return

    user = store.register_user(user_id, wallet_address)
    print_user_db(user_id)
    await ctx.send(f'{member.mention} been registered.\n'
                   f'You can send him deposits to '
                   f'`{user.actual_address.address}`.')


@bot.command(pass_context=True, help=bot_help_register)
async def register(ctx, wallet_address: str):
    print("************************REGISTER***************************")
    user_id = ctx.author.id
    print(user_id)
    print(wallet_address)
    if not (patter.match(wallet_address) and len(wallet_address) <= max_length):
        await ctx.send("Please use proper address!")
        return
    user_wallet = wallet.getWallet(user_id)
    print(user_wallet)
    if user_wallet is not None:
        existing_user = store.register_user(user_id)
        prev_address = existing_user.actual_address.address
        new_user = store.register_user(user_id, wallet_address)
        if prev_address:
            print_user_db(user_id)
            await ctx.send(
                f'Your deposit address has been changed from:\n'
                f'`{prev_address}`\n to\n '
                f'`{new_user.actual_address.address}`')
            return

    store.register_user(user_id, wallet_address)
    print_user_db(user_id)
    await ctx.send('You have been registered. You can ask admin to provide you tokens')


@bot.command(pass_context=True, help=bot_help_balance)
async def balance(ctx):
    print("************************BALANCE***************************")
    user_id = ctx.author.id
    print(user_id)
    user = store.register_user(user_id)
    print_user_db(user_id)
    wallet = store.get_user_wallet(user.user_id)
    if wallet.wallet_address.address is None:
        await ctx.send('Please register your wallet using $register')
    else:
        await ctx.send('**Your balance**\n\n'
                       f'Available: {wallet.balance / BISON_DIGITS} '
                       f'{BISON_REPR}\n')


# @bot.command(pass_context=True, help=bot_help_withdraw)
# async def withdraw(ctx, amount: float):
#   user_id = ctx.author.id
#   print(user_id)
#   await bot.send_message(ctx.author)

@bot.command(pass_context=True, help=bot_help_tip)
async def tip(ctx, member: discord.Member, amount: float):
    print("************************TIP***************************")
    user_id = ctx.author.id
    print(user_id)

    if (amount <= 0):
        await ctx.send(f'{ctx.author.mention} Don\'t be a fukin freak')
        return

    if user_id == member.id:
        await ctx.send(f'{ctx.author.mention} you are not allowed to tip yourself!')
        return

    user_from = store.register_user(user_id)

    if user_from.actual_address.address is None:
        await ctx.send(f'{ctx.author.mention} your wallet is not registered, please register using $register')
        return

    user_to = store.register_user(member.id)

    real_amount = int(amount * BISON_DIGITS)
    if user_to.actual_address.address is None:
        await ctx.send(f'{member.mention} wallet is not registered, please register using $register')
        return
    user_from_wallet = store.get_user_wallet(user_id)
    if real_amount >= user_from_wallet.balance:
        await ctx.send(f'Insufficient balance to send tip of '
                       f'{real_amount / BISON_DIGITS} '
                       f'{BISON_REPR} to {member.mention}.')
        return

    store.send_tip(user_from, user_to, real_amount)
    print_user_db(member.id)
    await ctx.send(
        f'Tip of {real_amount / BISON_DIGITS} '
        f'{BISON_REPR} '
        f'was sent to {member.mention}\n')


@bot.command(pass_context=True, help=bot_help_tip)
async def deposit(ctx, member: discord.Member, amount: float):
    print("************************ADD***************************")
    try:
        user_id = ctx.author.id
        print(user_id)
        print(member.id)
        if not (user_id == 968207994070368306 or user_id == 807103891182845992):
            await ctx.send("You are not allowed to give the initial tip")
            return
        user = store.register_user(member.id)
        if user.actual_address.address is None:
            await ctx.send(f'{member.mention} wallet is not registered yet!')
            return
        real_amount = int(amount * BISON_DIGITS)
        user = store.add(user, real_amount)
        print_user_db(member.id)
        await ctx.send(
            f'Added Balance {real_amount / BISON_DIGITS} '
            f'{BISON_REPR} '
            f'to {member.mention}\n')
    except:
        await ctx.send('Make sure you typed the command correct')
        raise


def print_user_db(user_id: str):
    db_address = wallet.getWallet(user_id)
    print("wallet address {0}".format(db_address))


# @withdraw.error
# async def withdraw_error(error, _: commands.Context):
#   await handle_errors(error, _)

@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.send(f'Invalid arguments provided.\n\n{err.args[0]}')
    if isinstance(err, error.AddressSyntexError):
        await ctx.send(f'Please provide address in correct format.\n\n{err.args[0]}')
    if isinstance(err, error.TokenNotFoundError):
        await ctx.send(f'Token not found.\n\n{err.args[0]}')
    if isinstance(err, error.WalletNotFoundError):
        await ctx.send(f'Wallet not found.\n\n{err.args[0]}')
    if isinstance(err, error.InsufficientAmountError):
        await ctx.send(f'Insufficient amount.\n\n{err.args[0]}')
    else:
        await ctx.send(f'Unexpected error.\n\n{err}')
    raise err


# async def update_balance_wallets():
#   while not bot.is_closed:
# store.update_balances()
# await asyncio.sleep(config.wallet_balance_update_interval)

@click.command()
def main():
    token = os.environ['BISON_BANK_KEY']
    bot.run(token)


if __name__ == '__main__':
    main()
