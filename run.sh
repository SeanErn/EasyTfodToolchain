#!/bin/bash

export GUM_CHOOSE_CURSOR_FOREGROUND="#EE4B2B"
export GUM_CHOOSE_PROMPT_FOREGROUND="#EE4B2B"
export GUM_INPUT_CURSOR_FOREGROUND="#6E260E"
export GUM_FILTER_PROMPT_FOREGROUND="#EE4B2B"
export GUM_FILTER_CURSOR_FOREGROUND="#6E260E"
# Install Gum
if ! command -v gum &> /dev/null
then
    echo "Run installDependencies.sh before continuing!"
    exit
fi

# PROJECT MANAGER

# create sub functions

# set project name
function setProjectName {
   directory=$1
   input=$1
   awk -v input="$input" '{
       sub(/PROJECT_NAME/, input);
       print;
   }' "$directory/config.json" > tmp && mv tmp "$directory/config.json"
}

# choose model
function chooseModelCheckpoint {
   directory=$1
   gum style --align left --width 50 --foreground "#EE4B2B" \
   'Setect the type of pretrained model to use as a base'
   input=$(cat availibleModels.txt | gum filter)
   awk -v input="$input" '{
       sub(/PRETRAINED_MODEL/, input);
       print;
   }' "$directory/config.json" > tmp && mv tmp "$directory/config.json"
   clear
}


# choose batch size
function chooseBatchSize {
   directory=$1
   gum style --align left --width 50 --foreground "#EE4B2B" \
   'Select the batch size you would like to use. In general, this should increase by 2 per 3GB of VRAM.'
   input=$(gum input --placeholder "ex. 2080ti has 11GB VRAM so batch size of 8")
   awk -v input="$input" '{
       sub(/BATCH_SIZE/, input);
       print;
   }' "$directory/config.json" > tmp && mv tmp "$directory/config.json"
   clear
}

# set training on tpu
function setTrainOnTpu {
    directory=$1
    gum style --align left --width 50 --foreground "#EE4B2B" \
   'Will you be training on a edgeTPU? A GPU is NOT an edgeTPU'
   input=$(gum choose true false)
   awk -v input=$input '{
       sub(/TRAIN_ON_TPU/, input);
       print;
   }' "$directory/config.json" > tmp && mv tmp "$directory/config.json"
   clear
}

# create
function createProject {
    gum style --align left --width 50 --foreground "#EE4B2B" \
    'Enter a name for your project'
    projectName=$(gum input --placeholder exampleProject)
    if [ ! -d $projectName ];
    then
        mkdir $projectName
        echo $projectName >> projectList.txt
        clear
        cp default.json "$projectName/config.json"
        chooseModelCheckpoint $projectName
        chooseBatchSize $projectName
        setProjectName $projectName
    else
        read -p "This project already exists! Press ENTER to return to menu."
    fi
}

# modify
function modifyProject {
    read -p "Not implemented. Press ENTER to return to menu."
}

# delete
function deleteProject {

    if [ ! -s "projectList.txt" ];
    then
        read -p "No projects exist! Press ENTER to return to menu."
    else
        project=$(cat projectList.txt | gum filter)
        gum confirm && ((rm -rf $project && sed -i /$project/d "projectList.txt") && read -p "Sucess! Press ENTER to return to menu.") || read -p "Operation Canceled. Press ENTER to return to menu."
    fi
    
}

# Project manager
function projectManager {
    cd projects
    action=$(gum choose CREATE MODIFY DELETE)
    clear
    case $action in
        "CREATE")
            createProject
            ;;
        "MODIFY")
            modifyProject
            ;;
        "DELETE")
            deleteProject
            ;;
        *)
            exit
            ;;
        esac
    
}

while true; do
    clear
    gum style --align left --width 50 --foreground "#EE4B2B" \
    'TensorFlow V2 Toolchain'
    gum style --align left --width 50 --foreground "#EE4B2B" \
    'Created by FRC Team 5152'
    gum style --align left --width 50  --foreground "#6E260E" \
    '************************'
    choice=$(gum choose "Install" "Project Manager" "Annotate" "Prepare Dataset" "Train Model" "Export Model" "Test Model" "Advanced" "Exit")
    case $choice in
        "Install")
            ./install.sh
            ;;
        "Project Manager")
            projectManager
            ;;
        "Annotate")
            labelImg 
            ;;
        *)
            exit
            ;;
        esac
    done
        