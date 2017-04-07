import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.io.*;
import java.util.regex.*;
import java.lang.Math;

/**
 *
 * @author profiterol
 */
public class Building {
    
    List<String> boxes = new ArrayList<String>();
    private List<String> offices = new ArrayList<String>();
    String robotLocation = "";
    List<String> dirtyLocations = new ArrayList<String>();
    Hashtable boxLocations = new Hashtable();
    String goalRobotLocation = "";
    Hashtable goalBoxLocations = new Hashtable();
    List<String> randomBoxesMoved = new ArrayList<String>();
    
    FileWriter fwPlan;
    BufferedWriter writerPlan;
    FileWriter fwGoal;
    BufferedWriter writerGoal;
    FileWriter fwStates;
    BufferedWriter writerStates;
        
    public void start(String fileName)
    {
        int d = 0; 
        // do until all boxes are moved
        int iterations = 0;
        String planFileName = fileName + "Plan.txt";
        String goalFileName = fileName + "Goal.txt"; 
        String statesFileName = fileName + "States.txt"; 
        
		try {
			fwPlan = new FileWriter(planFileName);
			writerPlan = new BufferedWriter(fwPlan);
			
			fwGoal = new FileWriter(goalFileName);
			writerGoal = new BufferedWriter(fwGoal);
			
			fwStates = new FileWriter(statesFileName);
			writerStates = new BufferedWriter(fwStates);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        
        // do this iteration until all boxes are moved to their goal positions
        // or a max number of iterations is reached
        while (!checkGoalCompleted())
        {
            iterations++;

            // an appropriate box is found
            String newBox = findAppropriateBox();
            
            // after a max number of iterations is reached, keep the best solutions so far
            if (newBox.equals("") && (iterations > 100))
            	break;
            
            // if an appropriate box can not be found, the boxes are moved randomly to
            // change the current configuration of boxes so that an appropriate box can be found  
            while (newBox.equals(""))
            {      
                d = d % 4 + 1;   
                //moveClosestToGoal(d);
                moveSomeRandomly(d);
                newBox = findAppropriateBox();
            }
            
            // the location and the goal location of the box is found
            String boxLocation = boxLocations.get(newBox).toString();
            String boxGoal = goalBoxLocations.get(newBox).toString();
            
            // the robot is sent to the location
            if (!robotLocation.equals(boxLocation))
                moveLongDistance(boxLocation);

            // the box is moved to its goal or closest to its goal
            if (robotLocation.equals(boxLocation))
            {
                pushLongDistance(newBox, boxGoal);
            }
        }
        
        iterations = 0;
        // after all the boxes are moved check if any dirty office is left and
        // if yes, go clean them until all are clean
        while (!checkAllClean() && iterations < 100)
        {
            iterations++;
            
            // find the closest dirty
            String newDirty = findClosestDirty(robotLocation);
            
            // go to the dirty office location
            moveLongDistance(newDirty);
            
            // check if the robot is in the dirty location
            if (robotLocation.equals(newDirty))
            {
                if (checkPrec("Clean-office", robotLocation, "", "" ))
                {
                    performAction("Clean-office", robotLocation, "", ""); 
                }
            }  
        }
        
        // after the boxes are sent and dirty offices are cleaned sent the robot to its final 
        // position
        
        if (!robotLocation.equals(goalRobotLocation))
        {
            moveLongDistance(goalRobotLocation);
        }
        
        try {
        	writeFinalStack();
			writerPlan.close();
	        writerGoal.close();
	        writerStates.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }
     
    // This function checks preconditions for a given action and parameters. 
    public boolean checkPrec(String action, String arg1, String arg2, String arg3)
    {
        if (action.equals("Clean-office")) // arg1 = o1; arg2, arg3 = "" (not used)
        {
            boolean cond1 = robotLocation.equals(arg1); // robot-location(o)
            boolean cond2 = dirtyLocations.contains(arg1); // dirty(o)
            boolean cond3 = !(boxLocations.containsValue(arg1)); // empty(o)
            
            return cond1 && cond2 && cond3;
        }
        else if (action.equals("Move")) // arg1 = o1; arg2 = o2; arg3 = ""
        {
            boolean cond1 = robotLocation.equals(arg1); // robot-location(o1) 
            boolean cond2 = isAdjacent(arg1, arg2); // adjacent(o1,o2)
            
            return cond1 && cond2;
        }
        else if (action.equals("Push")) // arg1 = o1; arg2 = o2; arg3 = box
        {
            boolean cond1 = robotLocation.equals(arg1); // robot-location(o1) 
            boolean cond2 = boxLocations.get(arg3).equals(arg1); // box-location(b,o1)
            boolean cond3 = isAdjacent(arg1, arg2); // adjacent(o1,o2)
            boolean cond4 = !(boxLocations.containsValue(arg2)); // empty(o2)
            
            return cond1 && cond2 && cond3 && cond4;
        }
        else        
            return false;       
    }
    
    // This functions performs the action with the given parameters and is called only after 
    // the preconditions are checked. It adds and deletes the relevant predicates. 
    public void performAction(String action, String arg1, String arg2, String arg3)
    {
    	String content = "";
    	String stateChanges = "";
        if (action.equals("Clean-office")) // arg1 = o1; arg2, arg3 = "" (not used)
        {
            dirtyLocations.remove(arg1); // delete: dirty(o)        
            // add actions: clean(o) are done implicitly.    
            content = action + "(" + arg1 + ")\n";
            stateChanges = "delete: dirty(" + arg1 + ")\n";
            
        }
        else if (action.equals("Move")) // arg1 = o1; arg2 = o2; arg3 = ""
        {
            robotLocation = arg2; // add: robot-location(o2) 
            // delete actions: robot-location(o1) are done implicitly. 
            content = action + "(" + arg1 + "," + arg2 + ")\n";
            stateChanges = "delete: robot-location(" + arg1 + ")\n";
            stateChanges = stateChanges + "add: robot-location(" + arg2 + ")\n";
        }
        else if (action.equals("Push")) // arg1 = o1; arg2 = o2; arg3 = box
        {
            boxLocations.put(arg3, arg2); // add: box-location(b,o2), empty(o1)(implicit)
            robotLocation = arg2; // add: robot-location(o2)
            // delete actions: empty(o2), box-location(b,o1), robot-location(o1)
            // are done implicitly 
            content = action + "(" + arg1 + "," + arg2 + "," + arg3 +")\n";
            stateChanges = "delete: box-location(" + arg3 + "," + arg1 + ")\n";
            stateChanges = stateChanges + "delete: robot-location(" + arg1 + ")\n";
            stateChanges = stateChanges + "add: box-location(" + arg3 + "," + arg2 + ")\n";
            stateChanges = stateChanges + "add: robot-location(" + arg2 + ")\n";      
        }
        
        try {
			writerPlan.write(content);
			writerStates.write(content);
			writerStates.write(stateChanges);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        
    }
    
    // this function is created for convenience. Normally the robot can move one at a time.
    // this function is based on these single moves which are performed after the preconditions 
    // are checked
    public void moveLongDistance(String destination)
    {   
        int x = getXDirection(robotLocation, destination);
        int y = getYDirection(robotLocation, destination);
        String adj = "";
        while (x != 0)
        {
            adj = findXAdjacent(robotLocation, x);
            if (checkPrec("Move", robotLocation, adj, "" ))
            {
                performAction("Move", robotLocation, adj, ""); 
                if (x < 0)
                    x++;
                if (x > 0)
                    x--; 

                // On its way if the robot passes through a dirty office, cleans it.
                if (checkPrec("Clean-office", robotLocation, "", "" ))
                {
                    performAction("Clean-office", robotLocation, "", ""); 
                }
            }          
        }

        while (y != 0)
        {
            adj = findYAdjacent(robotLocation, y);
            if (checkPrec("Move", robotLocation, adj, "" ))
            {
                performAction("Move", robotLocation, adj, "");
                if (y < 0)
                    y++;
                if (y > 0)
                    y--;  
                
                // On its way if the robot passes through a dirty office, cleans it.
                if (checkPrec("Clean-office", robotLocation, "", "" ))
                {
                    performAction("Clean-office", robotLocation, "", ""); 
                }
            }

        }
    }
    
    // this function is created for convenience. Normally the robot can push one box
    // one office at a time this function is based on these single moves which are performed
    // after the preconditions are checked.
    public void pushLongDistance(String boxName, String destination)
    {
        int x = getXDirection(robotLocation, destination);
        int y = getYDirection(robotLocation, destination);
        int initX = x;
        int initY = y;

        while ((x != 0) || (y != 0))
        {   
            boolean moved = false;
            if (x != 0)
            {
                String adj = findXAdjacent(robotLocation, x);
                
                // if the next stop is dirty and does not contain boxes, clean it and get back
                // this is necessary because we are close to a dirty location it is good to clean 
                // it for the sake of efficiency. We cannot clean it after we push the box, 
                // because there will be a box on it.
                if (dirtyLocations.contains(adj) && !boxLocations.containsValue(adj))
                {
                    if (checkPrec("Move", robotLocation, adj, "" ))
                    {
                        String prevLocation = robotLocation;
                        performAction("Move", robotLocation, adj, "");
                        performAction("Clean-office", robotLocation, "", ""); 
                        performAction("Move", robotLocation, prevLocation, "");
                    }
                }
                
                // Push the box in the x direction
                if (checkPrec("Push", robotLocation, adj, boxName ))
                {
                    performAction("Push", robotLocation, adj, boxName); 
                    if (x < 0)
                        x++;
                    if (x > 0)
                        x--;   
                    moved = true;
                }
            }
            if (y != 0)
            {
                String adj = findYAdjacent(robotLocation, y);
                // if the next stop is dirty and does not contain boxes, clean it and get back
                // this is necessary because we are close to a dirty location it is good to clean 
                // it for the sake of efficiency. We cannot clean it after we push the box, 
                // because there will be a box on it.
                if (dirtyLocations.contains(adj) && !boxLocations.containsValue(adj))
                {
                    if (checkPrec("Move", robotLocation, adj, "" ))
                    {
                        String prevLocation = robotLocation;
                        performAction("Move", robotLocation, adj, "");
                        performAction("Clean-office", robotLocation, "", ""); 
                        performAction("Move", robotLocation, prevLocation, "");
                    }
                }
                
                // Push the box in the y direction
                if (checkPrec("Push", robotLocation, adj, boxName ))
                {
                    performAction("Push", robotLocation, adj, boxName);
                    if (y < 0)
                        y++;
                    if (y > 0)
                        y--; 
                    moved = true;
                }
            }
            
            // if the box could not be moved in x or y directions then it means it is blocked
            // in those directions. So we move the blocking box in the opposite direction 
            // of our destination.
            if (!moved)
            {
                if ((x != 0) && (initY != 0))
                {   
                    String prevLoc = robotLocation;
                    String adj = findXAdjacent(robotLocation, x);  
                    if (checkPrec("Move", robotLocation, adj, "" ))
                    {
                        String adjNew = findYAdjacent(adj, -initY);
                        
                        if (!adjNew.equals("") && !boxLocations.containsValue(adjNew))
                        {
                            performAction("Move", robotLocation, adj, "");
                            String newBox = findBoxName(robotLocation);
                            if (checkPrec("Push", robotLocation, adjNew, newBox))
                            {
                                performAction("Push", robotLocation, adjNew, newBox);
                               
                                moved = true;
                            }   
                            moveLongDistance(prevLoc);   
                        }       
                    }
                }
                
                if ((y != 0) && (initX != 0) && !moved)
                {
                    String prevLoc = robotLocation;
                    String adj = findYAdjacent(robotLocation, y);  
                    if (checkPrec("Move", robotLocation, adj, "" ))
                    {
                        String adjNew = findXAdjacent(adj, -initX);
                        
                        if (!adjNew.equals("") && !boxLocations.containsValue(adjNew))
                        {
                            performAction("Move", robotLocation, adj, "");
                            String newBox = findBoxName(robotLocation);
                            if (checkPrec("Push", robotLocation, adjNew, newBox))
                            {
                                performAction("Push", robotLocation, adjNew, newBox);
        
                                moved = true;
                            }
                            moveLongDistance(prevLoc);   
                        }   
                           
                    }
                }   
                if (!moved)
                    break;      
            }
        }

    }
    
    // This function checks if all boxes are sent to their final locations and returns 
    // true or false
    public boolean checkGoalCompleted()
    {
        Set<String> keys = boxLocations.keySet();
        for(String key: keys){
            String location = boxLocations.get(key).toString();
            String goal = goalBoxLocations.get(key).toString();
            if (!goal.equals(location))
                return false;
        }   
        return true;
    }
    
    // This function checks if all offices are clean.
    public boolean checkAllClean()
    {
        if (dirtyLocations.isEmpty())
            return true;
        else
            return false;
    }
    
    
    // This function finds if two offices are adjacent.
    public boolean isAdjacent(String arg1, String arg2)
    {
        int num1 = Integer.parseInt(arg1.replace("o", "")); // get the number of the location 1
        int num2 = Integer.parseInt(arg2.replace("o", "")); // get the number of the location 2
        
        int a1, a2;    
        if (num1 < num2) 
        { a1 = num1; a2 = num2; }
        else 
        { a1 = num2; a2 = num1; }
        
        if ((a1 % 3) == 0) // if the small number is on the right edge e.g :3, 6, 9
        {
            if (a2 == a1 + 3) 
                return true;
            else
                return false;
        }
        else
        {
            if ((a2 == a1 + 3) || (a2 == a1 + 1))
                return true;
            else
                return false;
        }    
    }
    
    // This function gets the distance between two offices.
    public int getDistance(String arg1, String arg2)
    {
        int num1 = Integer.parseInt(arg1.replace("o", "")); // get the number of the location 1
        int num2 = Integer.parseInt(arg2.replace("o", "")); // get the number of the location 2
        
        int x1 = ((num1 - 1) % 3) + 1;
        int y1 = ((num1 + 2) / 3);
        
        int x2 = ((num2 - 1) % 3) + 1;
        int y2 = ((num2 + 2) / 3);
        
        return Math.abs(x2 - x1) + Math.abs(y2 - y1);
    }
    
    // This function gets the x direction and distance given a location and a goal.
    // The sign of the return value gives the direction and the value the distance.
    public int getXDirection(String arg1, String arg2)
    {
        int num1 = Integer.parseInt(arg1.replace("o", "")); // get the number of the location 1
        int num2 = Integer.parseInt(arg2.replace("o", "")); // get the number of the location 2
        
        int x1 = ((num1 - 1) % 3) + 1;
        int x2 = ((num2 - 1) % 3) + 1;
        
        return x2 - x1;
    }
    
    // This function gets the y direction and distance given a location and a goal. 
    // The sign of the return value gives the direction and the value the distance.
    public int getYDirection(String arg1, String arg2)
    {
        int num1 = Integer.parseInt(arg1.replace("o", "")); // get the number of the location 1
        int num2 = Integer.parseInt(arg2.replace("o", "")); // get the number of the location 2
        
        int y1 = ((num1 + 2) / 3);
        int y2 = ((num2 + 2) / 3);
        
        return y2 - y1;
    }
    
    // This function finds the X adjacent of an office in the given direction. If x is positive,
    // the direction is to the right.
    public String findXAdjacent(String arg1, int x)
    {
        int num = Integer.parseInt(arg1.replace("o", ""));
        int newNum = num;
        if ((x > 0) && (num % 3 == 0))
            return "";
        if ((x < 0) && (num % 3 == 1))
            return "";
        if (x > 0)
            newNum = num + 1;
        else if (x < 0)
            newNum = num - 1;
        if ((newNum >= 0) && (newNum <=9))
            return "o" + newNum;
        else
            return "";
    }
    
    // This function finds the Y adjacent of an office in the given direction. If y is positive,
    // the direction is downwards.
    public String findYAdjacent(String arg1, int y)
    {
        int num = Integer.parseInt(arg1.replace("o", ""));
        int newNum = num;
        if ((y > 0) && (num > 6))
            return "";
        if ((y < 0) && (num < 4))
            return "";
        
        if (y > 0)
            newNum = num + 3;
        else if (y < 0)
            newNum = num - 3;
        
        if ((newNum >= 0) && (newNum <=9))
            return "o" + newNum;
        else
            return "";
    }
    
    // This function finds an appropriate box to be moved to its goal location 
    // which is movable in the goal direction. It gives priority to the boxes 
    // with goal positions in the corner.
    public String findAppropriateBox()
    {
        Set<String> keys = boxLocations.keySet();
        String location = "";
        String goal = "";
        String chosen = "";
        String secondChosen = "";
        String thirdChosen = "";
        for(String key: keys){
            location = boxLocations.get(key).toString();
            goal = goalBoxLocations.get(key).toString();
            int x = getXDirection(location, goal);
            int y = getYDirection(location, goal);
            String xAdj = findXAdjacent(location, x);
            String yAdj = findYAdjacent(location, y);
            boolean moveable = true;
            if (boxLocations.containsValue(xAdj) && boxLocations.containsValue(yAdj))
                moveable = false;
            
            if ((moveable) && (goal != location)) 
            {
                if (goal.equals("o1") || goal.equals("o3") || goal.equals("o7") || goal.equals("o9"))
                {
                    chosen = key;
                    break;
                }
                if (goal.equals("o2") || goal.equals("o4") || goal.equals("o6") || goal.equals("o8"))
                {
                    secondChosen = key;
                }
                if (goal.equals("o5"))
                {
                    thirdChosen = key;        
                }    
            }
        }
        if (!chosen.equals(""))
            return chosen; 
        else if (!secondChosen.equals(""))
            return secondChosen; 
        else
            return thirdChosen;
    }
    
    // This function finds the closest dirty location
    public String findClosestDirty(String arg1)
    {
        int dist = 20;
        int newDist = 0;
        String chosen = "";
        for(String loc: dirtyLocations){
           
            newDist = getDistance(arg1, loc); 
            if (newDist < dist)
            {
                dist = newDist; 
                chosen = loc;    
            }
        }
        return chosen; 
    }
    
    // This function finds the box name in a given office. 
    public String findBoxName(String loc)
    {
        Set<String> keys = boxLocations.keySet();
        String newBox = "";  
        String location = "";
        for(String key: keys){
            location = boxLocations.get(key).toString();
            if (loc.equals(location))
            {
                newBox = key;
                break;
            }
        }
        return newBox;
    }
    
    // This function moves some of the boxes randomly when there can not be any further
    // improvements
    public void moveSomeRandomly(int x)
    {
        Set<String> keys = boxLocations.keySet();
        String box = ""; 
        String location = "";
        String adj = "";
        for(String key: keys){
            location = boxLocations.get(key).toString();  
            adj = "";
            box = "";
            if (x == 1)
            {
                adj = findXAdjacent(location, 1);
                if (!adj.equals("") && !(boxLocations.containsValue(adj)))
                {
                    box = key;
                }
            }
            if (x == 3)
            {
                adj = findXAdjacent(location, -1);
                if (!adj.equals("") && !(boxLocations.containsValue(adj)))
                {
                    box = key;
                }
            }
            if (x == 2)
            {
                adj = findYAdjacent(location, 1);
                if ((!adj.equals("") && !(boxLocations.containsValue(adj))) )
                {
                    box = key;
                }
            }
            if (x == 4)
            {
                adj = findYAdjacent(location, 1);
                if ((!adj.equals("") && !(boxLocations.containsValue(adj))))
                {
                    box = key;
                }
            }
            if ((!adj.equals("")) && (!box.equals("")))
            {
                moveLongDistance(location);
                pushLongDistance(box, adj);
            }
        }
    }
    
    
    public void moveClosestToGoal(int d)
    {
        Set<String> keys = boxLocations.keySet();
        
        Boolean movedAtAll = false;
        for(String key: keys){
            String loc = "";
            String box = "";
            String orgBox = "";
            String moveTo = "";
            String orgLoc = "";
            Boolean moved = false;
            String location = boxLocations.get(key).toString();
            String goal = goalBoxLocations.get(key).toString();
            int dist = getDistance(location, goal);
            if (dist == 1)
            {
                String xAdjPos = findXAdjacent(goal, 1);
                String yAdjPos = findYAdjacent(goal, 1);
                String xAdjNeg = findXAdjacent(goal, -1);
                String yAdjNeg = findYAdjacent(goal, -1);

                if (boxLocations.containsValue(xAdjPos) || xAdjPos.equals(""))
                {
                    if (boxLocations.containsValue(xAdjNeg) || xAdjNeg.equals(""))
                    {
                        if (boxLocations.containsValue(yAdjPos) || yAdjPos.equals(""))
                        {
                            if (boxLocations.containsValue(yAdjNeg) || yAdjNeg.equals(""))
                            {
                                
                            }
                            else
                            {
                                loc = goal;
                                orgBox = key;
                                moveTo = yAdjNeg;
                                orgLoc = location;
                                moved = true;
                                movedAtAll = true;
                            }  
                        }
                        else
                        {
                            loc = goal;
                            orgBox = key;
                            moveTo = yAdjPos;
                            orgLoc = location;
                            moved = true;
                            movedAtAll = true;
                        }  
                    }
                    else
                    {
                        loc = goal;
                        orgBox = key;
                        moveTo = xAdjNeg;
                        orgLoc = location;
                        moved = true;
                        movedAtAll = true;
                    }  
                }
                else
                {
                    loc = goal;
                    orgBox = key;
                    moveTo = xAdjPos;
                    orgLoc = location;
                    moved = true;
                    movedAtAll = true;
                }  
                if (moved)
                {
                    moveLongDistance(loc);
                    box = findBoxName(loc);
                    if (checkPrec("Push", robotLocation, moveTo, box))
                    {
                        performAction("Push", robotLocation, moveTo, box); 
                    }
                    moveLongDistance(orgLoc);
                    if (checkPrec("Push", robotLocation, loc, orgBox))
                    {
                        performAction("Push", robotLocation, loc, orgBox); 
                    }
                }
            }
            
        }
        
        if (!movedAtAll)
            moveSomeRandomly(d);
    }

    // reads the configuration file
    public void readConfFile(String fileName)
    {
        BufferedReader br = null;

        try {

            String line;
            String prevLine = "";
            br = new BufferedReader(new FileReader(fileName));
                
            List<String> lines = new ArrayList<String>();
            while ((line = br.readLine()) != null) {
            	String[] parts = line.split("=");
                if (parts.length > 1) // if there is = symbol in the line
                {   
                    if (prevLine != "")
                        lines.add(prevLine);
                    prevLine = line.trim();
                }
                else
                    prevLine = prevLine + line.trim();
            }
            lines.add(prevLine);    
              
            Iterator iterator = lines.iterator();
            while(iterator.hasNext()){
                String element = (String) iterator.next();
                String[] parts = element.split("=");
                if (parts[0].equals("Boxes"))
                {
                    String[] words = parts[1].split(",");
                    for(int i = 0; i < words.length; i++)
                    {
                        boxes.add(words[i]);
                    }
                }
                else if (parts[0].equals("Offices"))
                {
                    String[] words = parts[1].split(",");
                    for(int i = 0; i < words.length; i++)
                    {
                        offices.add(words[i]);
                    }
                }
                else if (parts[0].equals("InitialState"))
                {
                    String[] words = parts[1].split(";");
                    for(int i = 0; i < words.length; i++)
                    {
                        Pattern p = Pattern.compile("[(](.*)[)]");
                        Matcher m = p.matcher(words[i]);
                        String item = "";
                        String function = "";
                        if (m.find())
                        {
                            item = m.group(1).trim();
                        }
                        
                        Pattern p2 = Pattern.compile("(.*)[(]");
                        Matcher m2 = p2.matcher(words[i]);
                        if (m2.find())
                        {
                            function = m2.group(1).trim();
                        }
                        
                        if (function.equals("Dirty"))
                        {
                            dirtyLocations.add(item);
                        }
                        
                        if (function.equals("Box-location"))
                        {
                            String[] w = item.split(",");
                            boxLocations.put(w[0].trim(), w[1].trim());
                        }
                        
                        if (function.equals("Robot-location"))
                        {
                            robotLocation = item;
                        }
                    }           
                    
                }
                else if (parts[0].equals("GoalState")) 
                {
                    String[] words = parts[1].split(";");
                    for(int i = 0; i < words.length; i++)
                    {
                        Pattern p = Pattern.compile("[(](.*)[)]");
                        Matcher m = p.matcher(words[i]);
                        String item = "";
                        String function = "";
                        if (m.find())
                        {
                            item = m.group(1).trim();
                        }
                        
                        Pattern p2 = Pattern.compile("(.*)[(]");
                        Matcher m2 = p2.matcher(words[i]);
                        if (m2.find())
                        {
                            function = m2.group(1).trim();
                        }
                        
                        if (function.equals("Box-location"))
                        {
                            String[] w = item.split(",");
                            goalBoxLocations.put(w[0].trim(), w[1].trim());
                        }
                        
                        if (function.equals("Robot-location"))
                        {
                            goalRobotLocation = item;
                        } 
                    }         
                }
            }       
		} catch (IOException e) {
			e.printStackTrace();
		}
    }
    
    // Writes the final stack
    public void writeFinalStack()
    {
    	
    	String locations = "Robot-location(" + robotLocation + ");";
    	
    	Set<String> keys = boxLocations.keySet();
        for(String key: keys){
            String location = boxLocations.get(key).toString();
            locations = locations + "Box-location(" + key + ", " + location +  ");";
        } 
        
        for(String loc: dirtyLocations){
            locations = locations + "Dirty(" + loc + ");";
        }
        
        try {
			writerGoal.write(locations);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
            
    }

}



