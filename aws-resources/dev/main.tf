locals {
  default_tags = {
    "Environment" = var.ENV,
    "Project"     = var.PREFIX,
    "CreatedBy"   = "kakimoto"
  }
}

module "vpc" {
  source            = "../modules/vpc"
  ENV               = var.ENV
  AWS_REGION        = var.AWS_REGION
  PREFIX            = var.PREFIX
  DEFAULT_TAGS      = local.default_tags
}

module "sg" {
  source            = "../modules/sg"
  ENV               = var.ENV
  AWS_REGION        = var.AWS_REGION
  PREFIX            = var.PREFIX
  DEFAULT_TAGS      = local.default_tags
  VPC_ID            = module.vpc.vpc_id
}

module "ecr" {
  source = "../modules/ecr"
}

module "iam" {
  source = "../modules/iam"
}

module "alb" {
  source            = "../modules/alb"
  ENV               = var.ENV
  AWS_REGION        = var.AWS_REGION
  PREFIX            = var.PREFIX
  DEFAULT_TAGS      = local.default_tags
  VPC_ID            = module.vpc.vpc_id
  PRIVATE_SUBNETS   = module.vpc.private_subnets
  PUBLIC_SUBNETS    = module.vpc.public_subnets
  ALB_SG_ID         = module.sg.alb_sg_id
//  DJANGO_SG_ID      = module.sg.django_sg_id
}


module "ecs" {
  source            = "../modules/ecs"
  ENV               = var.ENV
  AWS_REGION        = var.AWS_REGION
  PREFIX            = var.PREFIX
  DEFAULT_TAGS      = local.default_tags
  VPC_ID            = module.vpc.vpc_id
  PRIVATE_SUBNETS   = module.vpc.private_subnets
  PUBLIC_SUBNETS    = module.vpc.public_subnets
  ALB_SG_ID         = module.sg.alb_sg_id
  DJANGO_SG_ID      = module.sg.django_sg_id
  ALB_DEPEND        = module.alb.alb_depend
  ALB_TARGET_GROUP  = module.alb.alb_target_group
  ECR_REPO_URL      = module.ecr.ecr_repository_url
  ECS_TASK_ROLE     = module.iam.ecs_task_execution_role
}
