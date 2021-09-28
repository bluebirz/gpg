# create our keys
# https://docs.github.com/en/github/authenticating-to-github/managing-commit-signature-verification/generating-a-new-gpg-key
gpg --full-generate-keys

# if got error : no pinentry
# https://chaosfreakblog.wordpress.com/2013/06/21/gpg-problem-with-the-agent-no-pinentry-solved/
yum install pinentry

# list our keys
gpg --list-keys
gpg --list-secret-keys

# export keys
gpg --export -o folder/sample.gpg -a


# import keys
gpg --import sample.gpg

# trust keys
gpg --edit-key receiver@samplemail.com
gpg> trust
gpg> 5 (for dramatically trust person)
gpg> quit

# encrypt
gpg --output folder/message.txt.gpg --batch --yes --passphrase "pass1234" -e -r receiver@mail.com folder/message.txt

# checksum
sha256sum folder/message.txt | awk '{print $1}' > folder/message.checksum
gpg --output folder/message.checksum.sig --batch --yes --quiet --sign folder/message.checksum

# decrypt
gpg --output folder/message.txt --batch --yes --passphrase "pass1234" --decrypt folder/message.txt.gpg

# verify checksum
gpg --verify folder/message.checksum.sig
gpg --output folder/message.checksum --decrypt folder/message.checksum.sig

