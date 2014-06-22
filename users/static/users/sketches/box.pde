float x, y, z;
float angle_x=0, angle_y=0, angle_z=0;

void setup()
{
   size(200, 200, P3D);
   x = width/2;
   y = height/2;
   z = 0; 
}


void draw()
{
  background(#eeeeee);
  lights();
  translate(x, y, z);
  rectMode(CENTER);
 
  if (keyPressed)
    KeyPressHandle();
 
  rotateX(angle_x);
  rotateY(angle_y);
  rotateZ(angle_z);
   
  box(50);
//  rect(0, 0, 100, 100);
}

void KeyPressHandle()
{
  switch (key)
  {
    case 'q':
     angle_z -= PI/16;
     return;
    case 'w':
     angle_z += PI/16;
     return;
     case 'r':
      angle_x = 0;
      angle_y = 0;
      angle_z = 0;
      return; 
  }
  
  if (key != CODED)
    return;
  switch (keyCode)
  {    
   case UP:
    angle_x += PI/16;
    break;
   case DOWN:
    angle_x -= PI/16;
    break;
   case LEFT:
    angle_y -= PI/16;
    break;
   case RIGHT:
    angle_y += PI/16;
    break; 
  }
    
   
  
}
