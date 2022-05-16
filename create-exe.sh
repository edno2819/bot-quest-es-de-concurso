#Cmod +x creat-exe.sh - Dar permisão de execução para o script
# ./name - Executar um script
#Não pode haver espaços na declaração das variáveis

# Declaração
DIRETORIO=$PWD
PATH_VENV=$DIRETORIO'/venv/bin/activate'
NAME_FOLDER="Extrator"
NAME_FILE="Extrator Concurso"
DESK='/home/edno/Desktop'
FOLDER_EXE=$DESK'/'"$NAME_FOLDER"

#files to delete
FOLDERS_TO_DELETE=('build' 'dist')
FILE_TO_DELETE="${NAME_FILE}.spec"


source $PATH_VENV
mkdir -p $FOLDER_EXE"/logs"
pyinstaller --noconfirm --onefile --windowed --name "Extrator Concurso" --add-data "/home/edno/Desktop/jobs/bot-quest-es-de-concurso/configs.ini:."  "/home/edno/Desktop/jobs/bot-quest-es-de-concurso/Gui.py"
mv "dist/""$NAME_FILE" $FOLDER_EXE

for FileName in "${FOLDERS_TO_DELETE[@]}"; do   
    rm -r $FileName
done

rm "$FILE_TO_DELETE"