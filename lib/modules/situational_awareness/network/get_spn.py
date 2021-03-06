from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Get-SPN',

            'Author': ['@_nullbind'],

            'Description': ('Displays Service Principal Names (SPN) for domain accounts '
                            'based on SPN service name, domain account, or domain group '
                            'via LDAP queries.'),

            'Background' : True,

            'OutputExtension' : None,
            
            'NeedsAdmin' : False,

            'OpsecSafe' : True,
            
            'MinPSVersion' : '2',
            
            'Comments': [
                'https://raw.githubusercontent.com/nullbind/Powershellery/master/Stable-ish/Get-SPN/Get-SPN.psm1'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Type' : {
                'Description'   :   "'group', 'user', or 'service'",
                'Required'      :   False,
                'Value'         :   'service'
            },
            'Search' : {
                'Description'   :   'Search string for group, username, or service name. Wildcards accepted.',
                'Required'      :   False,
                'Value'         :   'MSSQL*'
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self):
        
        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/situational_awareness/Network/Get-SPN.ps1"

        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        script = moduleCode

        script += "\nGet-SPN"

        for option,values in self.options.iteritems():
            if option.lower() != "agent":
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == "true":
                        # if we're just adding a switch
                        script += " -" + str(option)
                    else:
                        script += " -" + str(option) + " " + str(values['Value']) 
        
        script += " -List yes | Format-Table -Wrap | Out-String | %{$_ + \"`n\"}"

        return script