(define (problem mixed_f8_p4_u0_v0_d0_a0_n0_a0_b0_n0_f0_problem_problem_problem_problem-problem)
 (:domain mixed_f8_p4_u0_v0_d0_a0_n0_a0_b0_n0_f0_problem_problem_problem_problem-domain)
 (:objects
   p0 p1 p2 p3 - passenger
   f0 f1 f2 f3 f4 f5 f6 f7 - floor
 )
 (:init (above f0 f1) (above f0 f2) (above f0 f3) (above f0 f4) (above f0 f5) (above f0 f6) (above f0 f7) (above f1 f2) (above f1 f3) (above f1 f4) (above f1 f5) (above f1 f6) (above f1 f7) (above f2 f3) (above f2 f4) (above f2 f5) (above f2 f6) (above f2 f7) (above f3 f4) (above f3 f5) (above f3 f6) (above f3 f7) (above f4 f5) (above f4 f6) (above f4 f7) (above f5 f6) (above f5 f7) (above f6 f7) (origin p0 f4) (destin p0 f6) (origin p1 f6) (destin p1 f3) (origin p2 f2) (destin p2 f1) (origin p3 f1) (destin p3 f7) (lift_at f0))
 (:goal (and (served p0) (served p1) (served p2) (served p3)))
)