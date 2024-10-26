from bip_utils import Bip39SeedGenerator, Bip39MnemonicValidator, Bip44, Bip44Coins, Bip44Changes
from aptos_sdk.account import Account

# Открываем файл с сид фразами
with open("mnemonics.txt", "r") as file:
    mnemonics = file.readlines()

# Открываем файлы для записи кошельков и ключей
with open("wallets.txt", "w") as wallets_file, open("privatekeys.txt", "w") as keys_file:
    # Обрабатываем каждую фразу
    for index, mnemonic in enumerate(mnemonics, start=1):
        mnemonic = mnemonic.strip()
        
        # Проверяем валидность мнемоники
        if not Bip39MnemonicValidator().IsValid(mnemonic):
            print(f"Неверная мнемоника: {mnemonic}")
            continue

        # Генерируем seed и используем его для создания аккаунта Aptos
        seed = Bip39SeedGenerator(mnemonic).Generate()
        bip44_def_ctx = Bip44.FromSeed(seed, Bip44Coins.APTOS)
        bip44_acc_ctx = bip44_def_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        
        # Создаем Account
        private_key = bip44_acc_ctx.PrivateKey().Raw().ToHex()
        account = Account.load_key(private_key)
        account_address = account.address()  # Получаем адрес аккаунта

        # Записываем результаты в файлы
        wallets_file.write(f"{account_address}\n")
        keys_file.write(f"{private_key}\n")

        print(f"Кошелек #{index}:")
        print(f"Приватный ключ: {private_key}")
        print(f"Номер аккаунта: {account_address}")
        print()

print("Генерация завершена. Номера кошельков сохранены в wallets.txt, а приватные ключи — в privatekeys.txt.")
