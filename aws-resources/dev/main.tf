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
  VPC_CIDR_BLOCK    = module.vpc.vpc_cidr_block
}

module "ecr" {
  source = "../modules/ecr"
}

module "iam" {
  source = "../modules/iam"
}

module "rds" {
  source = "../modules/rds"
  ENV               = var.ENV
  AWS_REGION        = var.AWS_REGION
  PREFIX            = var.PREFIX
  DEFAULT_TAGS      = local.default_tags
  VPC_ID            = module.vpc.vpc_id
  TEMP_SG_ID        = module.sg.temp_sg_id
  PUBLIC_SUBNETS    = module.vpc.public_subnets
  PRIVATE_SUBNETS   = module.vpc.private_subnets
  DB_SUBNET_GROUP   = module.vpc.database_subnet_group
  DB_SG_ID          = module.sg.db_sg_id
  USERNAME          = var.USERNAME
  PASSWORD          = var.PASSWORD
  APP_USER          = var.APP_USER
  APP_PASS          = var.APP_PASS
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

output "vpc_info" {
  description = "vpc info"
  value = {
    "vpc_id"          = module.vpc.vpc_id
    "public_subnets"  = module.vpc.public_subnets
    "private_subnets" = module.vpc.private_subnets
    "vpc_cidr_block"  = module.vpc.vpc_cidr_block
  }
}

output "ecr_info" {
  description = "ecr info"
  value = {
    "ecr_repository_url" = module.ecr.ecr_repository_url
  }
}

output "ecs_task_iam_role" {
  description = "ecs task iam role"
  value = {
    "ecs_task_iam_role": module.iam.ecs_task_execution_role
  }
}


