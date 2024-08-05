(define (problem dlog_3_3_3_problem_problem-problem)
 (:domain dlog_3_3_3_problem_problem-domain)
 (:objects
   s0 s1 s2 s3 s4 s5 p0_1 p0_2 p0_3 p0_5 p1_0 p1_3 p2_3 p2_4 p2_5 p4_0 - location
   driver1 driver2 driver3 - driver
   truck1 truck2 truck3 - truck
   package1 package2 package3 - obj
 )
 (:init (at_ driver1 s1) (at_ driver2 s0) (at_ driver3 s0) (at_ truck1 s2) (empty truck1) (at_ truck2 s5) (empty truck2) (at_ truck3 s1) (empty truck3) (at_ package1 s4) (at_ package2 s5) (at_ package3 s3) (path s0 p0_1) (path p0_1 s0) (path s1 p0_1) (path p0_1 s1) (path s0 p0_2) (path p0_2 s0) (path s2 p0_2) (path p0_2 s2) (path s0 p0_3) (path p0_3 s0) (path s3 p0_3) (path p0_3 s3) (path s0 p0_5) (path p0_5 s0) (path s5 p0_5) (path p0_5 s5) (path s1 p1_3) (path p1_3 s1) (path s3 p1_3) (path p1_3 s3) (path s2 p2_3) (path p2_3 s2) (path s3 p2_3) (path p2_3 s3) (path s2 p2_4) (path p2_4 s2) (path s4 p2_4) (path p2_4 s4) (path s2 p2_5) (path p2_5 s2) (path s5 p2_5) (path p2_5 s5) (path s4 p4_0) (path p4_0 s4) (path s0 p4_0) (path p4_0 s0) (link s0 s1) (link s1 s0) (link s0 s3) (link s3 s0) (link s1 s3) (link s3 s1) (link s1 s5) (link s5 s1) (link s2 s1) (link s1 s2) (link s2 s5) (link s5 s2) (link s3 s4) (link s4 s3) (link s3 s5) (link s5 s3) (link s4 s0) (link s0 s4) (link s4 s1) (link s1 s4) (link s4 s2) (link s2 s4) (link s5 s4) (link s4 s5))
 (:goal (and (at_ driver1 s5) (at_ driver2 s4) (at_ driver3 s2) (at_ truck1 s3) (at_ truck3 s2) (at_ package1 s5) (at_ package2 s0) (at_ package3 s1)))
)
