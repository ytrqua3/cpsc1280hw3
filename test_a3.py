import unittest
import uuid
import os
import shutil
import subprocess
import stat
import re

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        set_of_tests = {"part1" : {"fut" :"script3_1.sh", "aux" :[]},
                        "part2" : {"fut" :"script3_2.sh", "aux" :["setup.sh"]},
                        "part3" : {"fut" :"script3_3.sh", "aux" :[]},
                        "part4" : {"fut" :"script3_4.sh", "aux" :[]}}
                        
        cls.shell = "/usr/bin/bash"
        cls.assertTrue(os.path.isfile(cls.shell), "/usr/bin/bash not found. Operating System my not be correct, considering using cloud9")

        cls.test = set_of_tests
        
        #Create temp directory
        uidString = str(uuid.uuid4()) 
        cls.test_directory = "/tmp/Assignment3_"+uidString;
        os.mkdir(cls.test_directory)
        
        #copy files to temp directory
        for test in set_of_tests:
            
            shutil.copy(cls.test[test]["fut"],cls.test_directory)
            os.system("chmod +x " + cls.test[test]["fut"])
            for file in cls.test[test]["aux"]:
                #copy files, and set permissions
                if os.path.isfile(file) : 
                    shutil.copy(file,cls.test_directory)
                    new_filename = cls.test_directory + "/" + file;
                    
                else:
                    print("Setup failed, file " + file + "Does not exist")
                    assert("Setup failed, file " + file + "Does not exist")
        
        os.chdir(cls.test_directory) 
        
        
        
    @classmethod
    def tearDown(cls):
        #shutil.rmtree(cls.test_directory)
        pass

    def test_script3_1(self):
        excutable_script = self.test["part1"]["fut"]
        print("Output for " + excutable_script)
        self.assertTrue(os.path.isfile(excutable_script),excutable_script+" file not found")
        test_dir = "p1_test"
        
        #create testing directory structure
        os.mkdir(test_dir)
        dirs = ["sub1", "sub2","finnikn"]
        filelist = [["fan.txt", "fun.txt", "fern.txt","fit.txt"],["non.txt", "fin.txt", "fuun.txt"],[]]
        filelist2 = ["fan.txt", "fun.txt", "fern.txt","fit.txt"];
        
        for f in filelist2:
            cmd = "echo test > " + test_dir + "/" + f
            os.system(cmd)
            
        for i in range(len(dirs)) :
            if not dirs[i] == "." :
                os.mkdir(test_dir+"/"+dirs[i])
            for file in filelist[i]:
                cmd = "echo test > " + test_dir+"/"+dirs[i]+"/"+file
                os.system(cmd)
        
        output_filename = "out3_1.txt"
        pattern = "f*n.txt"
        
        cpi = subprocess.run([self.shell, excutable_script,test_dir, pattern, output_filename], capture_output=True, text=True)
        
        #check output file has been created
        self.assertTrue(os.path.isfile(output_filename),"Output file was not created by the script")
        #read the output file
        expectedFiles = ["p1_test/sub1/fan.txt","p1_test/sub1/fun.txt","p1_test/sub1/fern.txt", "p1_test/sub2/fin.txt", "p1_test/sub2/fuun.txt"]
       
        with open(output_filename,"r") as file_handle:
            text = file_handle.read();
            print("Contents of output file:")
            print(text)
            lines  = text.strip().split("\n")
            self.assertTrue(len(lines) == len(expectedFiles),"Incorrect number of files found")
        
            line_pattern = "^[0-9]+ [-d][rwx-]{9} .*$"
        
            for line in lines:
                pair = line.split();
                idx = expectedFiles.index(pair[2])
                print("Checking format of:  " + line)                
                self.assertIsNotNone(re.match(line_pattern, line),"Format of output is incorrect")                
                
                print("Checking inode of :  " + pair[2])                
                self.assertTrue(str(os.stat(pair[2]).st_ino) == pair[0],"one or more inode numbers are incorrect")
        
            print("End of run")
        
    #Test number 2
    def test_script3_2(self):
        test_script = self.test["part2"]["fut"]
        print("Output for " + test_script)        
        self.assertTrue(os.path.isfile(test_script),"script3_2.sh file not found")
        
        test_dir = "p2_test"
        os.mkdir(test_dir)
        
        dirs = ["sub1", "sub2"]
        filelist = [[{"name":"fan.txt","perm":"o+x,u+r"}, {"name":"fun.txt","perm":"o+x,u-r"}, 
                     {"name":"fern.txt","perm":"o-x,u+r"},{"name":"fit.txt","perm":"o-x,u-r"}],
                     [{"name":"non.txt","perm":"o+x,u+r"}, {"name":"fin.txt","perm":"o+x,u-r"}, 
                      {"name":"fuun.txt","perm":"o-x,u-r"}]]
        
        for i in range(len(dirs)) :
            os.mkdir(test_dir+"/"+dirs[i])
            for file in filelist[i]:
                filename = test_dir+"/"+dirs[i]+"/"+file["name"]
                cmd = "echo test > " + filename
                os.system(cmd)
                permcmd = "chmod " + file["perm"] + " " +filename
                os.system(permcmd)
        
        #add executable permissions to test file
        expectedFiles = [test_dir+"/"+dirs[0]+"/"+filelist[0][0]["name"], 
                         test_dir+"/"+dirs[1]+"/"+filelist[1][0]["name"]]        
        
        #search pattern
        pat = "*.txt"
        
        #create script
        script = "echo test $1"
        filename = "p2.sh"
        file = open(filename,"wt")
        file.write(script)
        file.close()
        os.system("chmod +x p2.sh")
        print("Running Script 2")
        
        cpi = subprocess.run([self.shell, test_script,test_dir, pat, filename], capture_output=True, text=True)
        lines = cpi.stdout.strip().split("\n")
        print("Output for script:")
        print(lines)
        #check the results
        self.assertTrue(len(lines) == len(expectedFiles), "Incorrect number of results")
        
        for line in lines:
            print("output line")
            print(line)
            tokens = line.split()
            self.assertTrue(tokens[0] == "test", "user script did not run")
            idx = expectedFiles.index(tokens[1])  #will assert, if not in list
            expectedFiles.remove(tokens[1])
        print("End of run")
        
    def test_script3_3(self):
        test_script = self.test["part3"]["fut"]
        print("Output for " + test_script)
        self.assertTrue(os.path.isfile(test_script),"script3_3.sh file not found")
       
        names = ["Brett", "Eddy"]
        answers = ["'New Jeans' is the self-titled debut extended play ($EP) by "+
                   "South Korean girl group Brett. It was released on August 1, 2022,"+
                   " by ADOR, a subsidiary of Hybe Corporation. Consisting of $(2 + 2)"+
                   " tracks, the EP draws from synth-pop, hip\\\\hop, and"+
                   ' "R&B" and infuses elements of 1990s/2000s musical styles.',
                   "'New Jeans' is the self-titled debut extended play ($EP) by "+
                   "South Korean girl group Eddy. It was released on August 1, 2022,"+
                   " by ADOR, a subsidiary of Hybe Corporation. Consisting of $(2 + 2)"+
                   " tracks, the EP draws from synth-pop, hip\\\\hop, and"+
                   ' "R&B" and infuses elements of 1990s/2000s musical styles.']
        for i in range(2):
            cpi = subprocess.run([self.shell, test_script,names[i]], capture_output=True, text=True)

            text = cpi.stdout.strip();
            
            print("Output for ./script3_3.sh " + names[i]);
            print(text)
            self.assertTrue(text == answers[i].strip(), "Incorrect output")
        print("End of run")

    def test_script3_4(self):
        test_script = self.test["part4"]["fut"]
        print("Output for " + test_script)
        self.assertTrue(os.path.isfile(test_script),"script3_4.sh file not found")
        
        test_dir = "p4_test"
        os.mkdir(test_dir)
        
        dirs = ["sub1", "sub2","sub1/inner1.txt"]
        filelist = [["fan.txt", "fun.txt", "fern.txt","fit.txt","sim.rat"],
                    ["nsn.txt", "fin.txt", "fuun.txt","lack.txt","txt.tack"],
                    ["outer.sub","inner.dub"]]

        for i in range(len(dirs)) :
            os.mkdir(test_dir+"/"+dirs[i])
            for file in filelist[i]:
                cmd = "echo test > " + test_dir+"/"+dirs[i]+"/"+file
                os.system(cmd)

        pat = "*.txt"
        expectedFiles = ["p4_test/sub1/fan.txt","p4_test/sub1/fun.txt","p4_test/sub1/fern.txt","p4_test/sub1/fit.txt",
                         "p4_test/sub2/nsn.txt","p4_test/sub2/fin.txt","p4_test/sub2/fuun.txt","p4_test/sub2/lack.txt"] 
        cpi = subprocess.run([self.shell, test_script,test_dir, pat], capture_output=True, text=True)
        print("stderr:\n" + cpi.stderr)
        print("stdout:\n" + cpi.stdout)
        
        lines = cpi.stdout.strip().split("\n")
        n = 3
        try:
            for line in lines[0:-1]:
                files = line.strip().split(" ")
                self.assertTrue(len(files) == n, "One of the printed lines does not contain 3 filenames")
                for file in files:
                    expectedFiles.remove(file.strip())
            lastlinefiles = lines[-1].strip().split(" ")
            for file in lastlinefiles:
                expectedFiles.remove(file)
        except:
            self.assertTrue(False,"File found that does not match pattern")
        self.assertTrue(len(expectedFiles) == 0, "Not all the expected files for the pattern were found")
        print("Done!")
        
       
if __name__ == '__main__':
    unittest.main()
    