# CV

Cipher vault

—/ encrypt files /—

ls >> <filename>

CV -e <filename> -p <pass> >> File Ciphered Successfully || File Not Found

ls >> <filename>.cipher 
	 <filename>

—/ decrypt files /—

CV -d <filename>.cipher -p <pass> -o <new-filename> —Default = “d_<filename>”

	| <filename>.cipher != valid = “File passed is NOT valid”
	| <pass> != valid = “Password is NOT correct”
	| !<filename>.cypher = “File NOT found”
	| otherwise = “File Deciphered Successfully”

ls  >> <filename>.cipher
	  <filename>
	  <new-filename>

—/ Folder wide usage /—
CV -er <foldername>
Encrypts all files in folder and creates individual ciphers

CV -dr <folder>
Decrypts all .cipher files present and skips invalid files

CV -v
Controls verbosity

CV —help
Displays flags and usage
[[ECHO]]

[[ECHO]]
