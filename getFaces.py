#takes single-object obj files, preferably with only triangles, 
#and converts them into a format readable by the importCollision 
#script in PSS. Non-triangular faces shouldn't break anything, 
#but haven't been tested. Can accept multiple files at once.

import sys
import os
from datetime import datetime


objPaths = sys.argv[1:]
logPath = os.getcwd() + "/output/importObj" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".lua"
sys.stdout = open(logPath, "w")

textWrapping = False

for path in range(len(objPaths)):
    lines = []
    vertices = []
    faces = []
    print(objPaths[path], file=sys.stderr)
    if(os.path.splitext(objPaths[path])[1] == ".obj"):
        print("\n--", objPaths[path], ":", sep="")
        
        print("importObj(\n    {-100, 100, -100}, \n    {0, 0, 0}, ")
        
        f = open(objPaths[path], "r")
        for i in f:
          lines.append(i)
        f.close()

        #print("".join(lines))

        def readFile():
            for i in lines:
                if(i[0] == "#"):
                    #ignore comments
                    continue
                if(i[0] == "v"):
                    if(i[1] == "t" or i[1] == "n" or i[1] == "p"):#ignore texture coordinates, vertex normals, and space vertices
                        continue
                    else:
                        vertices.append(i.split()[1:])
                if(i[0] == "f"):
                    faces.append(i.split()[1:])
                    
            #print(vertices) 
            #print(faces)
            
            for i in range(len(faces)):
                faces[i][0] = faces[i][0].split("/")
                faces[i][1] = faces[i][1].split("/")
                faces[i][2] = faces[i][2].split("/")

            #print(faces)
            #print("Vertices:\n")
            print("    {", sep = "", end = "")
                
            for i in range(len(vertices)):
                if textWrapping:
                    print("\n        {", sep = "", end = "")
                else:
                    print("{", sep = "", end = "")
                print(", ".join(vertices[i]), sep = "", end = "}")
                if i < len(vertices)-1:
                    print(", ", sep = "", end = "")
            #print("}\n\n\nFaces:\n")

            if textWrapping:
                print("\n    }, \n    {\n        {", sep = "", end = "")
            else:
                print("}, \n    {{", sep = "", end = "")
                
            for i in range(len(faces)):
                for ii in range(len(faces[i])):
                    #print("\nE")
                    #print(faces[i][ii])
                    #print("F")
                    print(faces[i][ii][0], sep = ", ", end = "")
                    #print("G")
                    #print(", ".join(faces[i][ii]), sep = "", end = "}")
                    if ii < len(faces[i])-1:
                        print(", ", sep = "", end = "")
                if i < len(faces)-1:
                    
                    if textWrapping:
                        print("}, \n        {", sep = "", end = "")
                    else:
                        print("}, {", sep = "", end = "")

            if textWrapping:
                print("}\n    }\n)")
            else:
                print("}}\n)")
           
        readFile()
    else:
        if(os.path.splitext(objPaths[path])[1] == ".mtl"):
            print("    ignoring .mtl files", file=sys.stderr)
        else:
            print("    this is not an obj. ignoring", file=sys.stderr)
    print("    ", path+1, "/", len(objPaths), sep="", end="\n", file=sys.stderr)
print("\n\nFinished!", file=sys.stderr)
input()
