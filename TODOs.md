# ToDo:
## Missing Features:
- Add tests
- Add a proper warmup file
- Deliver better comments for the code
- Put the default values etc. into a seperate config file

## Missing "Workflows"
- Provide a proper way to start streamlit, not relying on the CLI. Since this is intended for windows a batch, shell, cmd or .exe as a file may be suitable to "launch" the interface amd open the browser
- Make the install as seamless as possible. Ensure all dependencies and imports are all caught via another script / workflow. Make this a one-stop-install if possible. 
  - For this to work I'll need to differentiate between Linux and Windows. Autodetection of GPUs would also be needed for the correct Wheels / CUDA. However, this isn't really my job...
  - Easiest would be to have an .exe
  - Streamlit can be formed into a standalone .exe using nativefier (see https://discuss.streamlit.io/t/streamlit-deployment-as-an-executable-file-exe-for-windows-macos-and-android/6812 for context)
  - However this doesnt matter too much for now