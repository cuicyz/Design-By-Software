void collision2D(char mode,double alpha, double R,
                 double m1, double m2, double r1, double r2,
                 double& x1, double& y1, double& x2, double& y2,
                 double& vx1, double& vy1, double& vx2, double& vy2,
                 int& error )     {

       double  r12,m21,d,gammav,gammaxy,dgamma,dr,dc,sqs,t,
               dvx2,a,x21,y21,vx21,vy21,pi2,vx_cm,vy_cm;

//     ***initialize some variables ****
       pi2=2*acos(-1.0E0);
       error=0;
       r12=r1+r2;
       m21=m2/m1;
       x21=x2-x1;
       y21=y2-y1;
       vx21=vx2-vx1;
       vy21=vy2-vy1;

       vx_cm = (m1*vx1+m2*vx2)/(m1+m2) ;
       vy_cm = (m1*vy1+m2*vy2)/(m1+m2) ;

//     ****  return old positions and velocities if relative velocity =0 ****
       if ( vx21==0 && vy21==0 ) {error=1; return;}


//     *** calculate relative velocity angle             
       gammav=atan2(-vy21,-vx21);




//******** this block only if initial positions are given *********

       if (mode != 'f') {

       
       d=sqrt(x21*x21 +y21*y21);
       
//     **** return if distance between balls smaller than sum of radii ***
       if (d<r12) {error=2; return;}

//     *** calculate relative position angle and normalized impact parameter ***
       gammaxy=atan2(y21,x21);
       dgamma=gammaxy-gammav;
          if (dgamma>pi2) {dgamma=dgamma-pi2;}
           else if (dgamma<-pi2) {dgamma=dgamma+pi2;}
       dr=d*sin(dgamma)/r12;
       
//     **** return old positions and velocities if balls do not collide ***
       if (  (fabs(dgamma)>pi2/4 && fabs(dgamma)<0.75*pi2) || fabs(dr)>1 )   
           {error=1; return;}


//     **** calculate impact angle if balls do collide ***
       alpha=asin(dr);

       
//     **** calculate time to collision ***
       dc=d*cos(dgamma);
       if (dc>0) {sqs=1.0;} else {sqs=-1.0;}
       t=(dc-sqs*r12*sqrt(1-dr*dr))/sqrt(vx21*vx21+ vy21*vy21);
//    **** update positions ***
       x1=x1+vx1*t;
       y1=y1+vy1*t;
       x2=x2+vx2*t;
       y2=y2+vy2*t;

       
   }

//******** END 'this block only if initial positions are given' *********
      
       
       
//     ***  update velocities ***

       a=tan( gammav +alpha);

       dvx2=-2*(vx21 +a*vy21) /((1+a*a)*(1+m21));
       
       vx2=vx2+dvx2;
       vy2=vy2+a*dvx2;
       vx1=vx1-m21*dvx2;
       vy1=vy1-a*m21*dvx2;

//     ***  velocity correction for inelastic collisions ***
	   
       vx1=(vx1-vx_cm)*R + vx_cm;
       vy1=(vy1-vy_cm)*R + vy_cm;
       vx2=(vx2-vx_cm)*R + vx_cm;
       vy2=(vy2-vy_cm)*R + vy_cm;
       

       return;
}