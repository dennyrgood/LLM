# Managing Ollama Environment Variables in NSSM

Extracted from PDF: Managing Ollama Environment Variables in NSSM.pdf

---

Managing Ollama Environment Variables
in NSSM
When the Ollama server is installed and managed by NSSM (Non-Sucking Service
Manager) as a Windows Service, standard system environment variables (set via the Windows
GUI or setx) are often ignored.
To permanently set the OLLAMA_KEEP_ALIVE variable and prevent Ollama from shutting down
after 5 minutes of inactivity, the variable must be injected directly into the NSSM service
configuration.

Prerequisite: Find the Service and NSSM
Step 1: Identify the Service Name
1.​ Press Win + R, type services.msc, and press Enter to open the Windows Services
Manager.
2.​ Locate the service associated with Ollama.
3.​ Right-click the service, select Properties, and confirm the Service name is ollama.
This is crucial for the next steps.
4.​ If the service is running, select the service and click Stop.

Step 2: Locate the NSSM Executable
You have confirmed the nssm.exe executable is located at D:\misc\nssm.exe and the service
name is ollama.
●​ Open Command Prompt or PowerShell (Run as Administrator).
●​ You will run the configuration commands using the full path: d:\misc\nssm <command>
ollama.

Method 1: Inject Variable via NSSM Command Line
(Recommended)
This method directly sets the variable using a single command.
Example (using your confirmed path and service name):
d:\misc\nssm set ollama AppEnvironmentExtra OLLAMA_KEEP_ALIVE -1​
●​ OLLAMA_KEEP_ALIVE: The variable name.
●​ -1: The value, which instructs Ollama to keep the running model loaded indefinitely,
preventing the 5-minute timeout.

Method 2: Inject Variable via NSSM Graphical User

Interface (GUI)
If you prefer a visual approach, you can use the NSSM edit GUI.
1.​ Open Command Prompt or PowerShell (Run as Administrator).
2.​ Run the edit command using your confirmed path and service name:​
d:\misc\nssm edit ollama​
3.​ The NSSM Configuration window will open. Navigate to the Environment tab (it's often
one of the tabs on the far right).
4.​ In the main text area, add the following line:​
OLLAMA_KEEP_ALIVE=-1​
​
(Note: Ensure this is the only entry if you want to replace existing environment variables,
or simply add it to the list if the text area is not blank).
5.​ Click OK to save the changes.

Final Steps: Restart and Verify
Step 3: Start the Service
1.​ Return to the Services Manager (services.msc).
2.​ Right-click the Ollama service and select Start.

Step 4: Verify the Timeout Setting
1.​ Open your terminal and run a model to ensure it is active:​
ollama run llama3:8b ""​
2.​ Immediately check the model status using the ps command:​
ollama ps​
The UNTIL column for the loaded model should now show a value of Forever, confirming that
the OLLAMA_KEEP_ALIVE=-1 environment variable was successfully applied to the NSSM
service.

