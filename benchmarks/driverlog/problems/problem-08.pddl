(define (problem dlog_3_3_3_problem_problem-problem)
 (:domain dlog_3_3_3_problem_problem-domain)
 (:objects
   s0 s1 s2 s3 s4 s5 p0_1 p0_4 p1_2 p1_4 p2_3 p3_0 p3_1 p3_5 p5_1 p5_3 p5_4 - location
   driver1 driver2 driver3 - driver
   truck1 truck2 truck3 - truck
   package1 package2 package3 - obj
 )
 (:init (at_ driver1 s3) (at_ driver2 s4) (at_ driver3 s0) (at_ truck1 s0) (empty truck1) (at_ truck2 s0) (empty truck2) (at_ truck3 s2) (empty truck3) (at_ package1 s4) (at_ package2 s0) (at_ package3 s3) (path s0 p0_1) (path p0_1 s0) (path s1 p0_1) (path p0_1 s1) (path s0 p0_4) (path p0_4 s0) (path s4 p0_4) (path p0_4 s4) (path s1 p1_2) (path p1_2 s1) (path s2 p1_2) (path p1_2 s2) (path s1 p1_4) (path p1_4 s1) (path s4 p1_4) (path p1_4 s4) (path s2 p2_3) (path p2_3 s2) (path s3 p2_3) (path p2_3 s3) (path s3 p3_0) (path p3_0 s3) (path s0 p3_0) (path p3_0 s0) (path s3 p3_1) (path p3_1 s3) (path s1 p3_1) (path p3_1 s1) (path s3 p3_5) (path p3_5 s3) (path s5 p3_5) (path p3_5 s5) (path s5 p5_1) (path p5_1 s5) (path s1 p5_1) (path p5_1 s1) (path s5 p5_4) (path p5_4 s5) (path s4 p5_4) (path p5_4 s4) (link s0 s3) (link s3 s0) (link s0 s4) (link s4 s0) (link s0 s5) (link s5 s0) (link s1 s0) (link s0 s1) (link s1 s5) (link s5 s1) (link s2 s0) (link s0 s2) (link s2 s1) (link s1 s2) (link s2 s4) (link s4 s2) (link s3 s5) (link s5 s3) (link s4 s1) (link s1 s4) (link s5 s4) (link s4 s5))
 (:goal (and (at_ driver1 s5) (at_ driver2 s0) (at_ driver3 s0) (at_ truck1 s0) (at_ truck2 s5) (at_ truck3 s5) (at_ package1 s3) (at_ package2 s3) (at_ package3 s0)))
)
