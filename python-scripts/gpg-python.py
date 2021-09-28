import os
import gnupg
import logging

# cr: https://www.saltycrane.com/blog/2011/10/python-gnupg-gpg-example/
# cr: https://docs.red-dove.com/python-gnupg/#deleting-keys
gnupghome = "folder/.gpg"

def gpg_create(home=gnupghome):
    gpg = gnupg.GPG(gnupghome=home)
    logging.info(gnupg.__version__)
    input_data = gpg.gen_key_input(name_email='adam@samplemail.com')
    key = gpg.gen_key(input_data)
    logging.info(key)

def gpg_get_publickey(home=gnupghome):
    gpg = gnupg.GPG(gnupghome=home)
    return gpg.list_keys()

def gpg_get_privatekey(home=gnupghome):
    gpg = gnupg.GPG(gnupghome=home)
    return gpg.list_keys(True)

def gpg_list(home=gnupghome):
    logging.info("list pub keys")
    logging.info(gpg_get_publickey(home))
    print("list priv keys")
    print(gpg_get_privatekey(home))

def gpg_export(output_folder, home=gnupghome):
    gpg = gnupg.GPG(gnupghome=home)
    gpg_personal_keyid = gpg_get_privatekey(home=gnupghome)[0]['keyid']
    logging.info("found keyid: " + gpg_personal_keyid)

    with open(os.path.join(output_folder, "bluebirz_public.asc"), "w") as f:
        f.write(gpg.export_keys(gpg_personal_keyid))
    
    with open(os.path.join(output_folder, "bluebirz_private.asc"), "w") as f:
        f.write(gpg.export_keys(gpg_personal_keyid, True))

def gpg_delete(id, home=gnupghome):
    gpg = gnupg.GPG(gnupghome=home)
    logging.info(str(gpg.delete_keys(id, True)))
    logging.info(str(gpg.delete_keys(id)))

def gpg_import(home, target_keyfile, trust_level = 'TRUST_ULTIMATE'):
    gpg = gnupg.GPG(gnupghome=home)
    with open(target_keyfile, 'rb') as f:
        key_data = f.read()
    import_result = gpg.import_keys(key_data)
    logging.info(import_result.results)
    target_fingerprint = import_result.results[-1]['fingerprint']
    gpg.trust_keys(target_fingerprint, trust_level)

def gpg_check_recipient(home, recipient):
    gpg = gnupg.GPG(gnupghome=home)
    all_keys = gpg.list_keys()
    target_recipient = [e for e in all_keys for u in e.get('uids') if recipient in u]

    if not target_recipient:
        logging.info("Not found: " + recipient)
        return False
    else:
        logging.info(str(target_recipient))
        return True

def gpg_decrypt(encrypted_filepath, decrypted_filepath, passphrase = "", home=gnupghome):
    gpg = gnupg.GPG(gnupghome=home)
    with open(encrypted_filepath, 'rb') as f:
        flag = gpg.decrypt_file(f, output=decrypted_filepath, passphrase=passphrase)
    logging.info(flag.ok, flag.status, flag.stderr)

def gpg_encrypt(home, original_filepath, encrypted_filepath, recipient, passphrase):
    gpg = gnupg.GPG(gnupghome=home)
    with open(original_filepath, 'rb') as f:
        data = f.read()
    encrypt_data = gpg.encrypt(data, passphrase=passphrase, recipients=recipient)
    logging.info(encrypt_data.ok, encrypt_data.status, encrypt_data.stderr)
    with open(encrypted_filepath, 'wb') as f:
        f.write(data)
