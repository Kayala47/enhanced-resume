# Using TagEditor

## Requirements:
- You'll need a Windows, 64-bit machine. It won't work on Mac, apparently :(


## Instructions
1. Open up the Tag Editor software by cd-ing into the target directory and running TagEditor.exe in the terminal
2. Copy your listings into the window. Make sure to separate listings by 5 spaces, minimum. 
3. Click the "start tagging" button once you're ready. You'll see a little pop-up, and you need to do the following:
    - In the "Dependencies" tab, unclick "Enable Dependencies"
    - In the "POS Tagging" tab, unclick "Enable POS Tagging"
    - In the "Categories" tab, unclick "Enable Categories"
    - In the "Named Entities" tab:
        + Make sure "Enable named entities" is clicked"
        + Click the radio button for Enter your entity labels
        + Enter "SKILL, ATTRIBUTE" into the text box. Don't enter the quotes, just the words themselves :)
4. Now, you should see the text you entered has been separated into paragraphs, and there is another pop-up next to it, containing the labels you entered. It should look like this:
![](tagging.png)

5. Tag all of the skills by clicking the "Skill" button and highlighting all the skill words. Then, click "Attribute" and highlight all attributes. 

6. For each listing, go to the starting sentence and right click, select "set new paragraph". You should see that line light up orange.
![](paragraphs.png)

7. Finally, click the "Create Data" button. Do the following for the pop-up:
    - Uncheck "Text", "Words", "Whitespaces", "Sentence starts"
    - In the "Named entities" row, click the radio button for "char" offset. 
    - In the column on the right, make sure to click the radio button for "manually assigned paragraphs".

![](create-data-settings.png)

8. Click "print on screen" and it should generate the "entities" part of the list. You'll still need to do the rest of the formatting, like adding the line number. Make sure that line number matches the line number of the row in the csv where you got the data.

9. All done!

