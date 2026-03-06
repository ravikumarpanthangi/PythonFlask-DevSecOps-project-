# ─────────────────────────────────────────────────────────────────────────────
#  Terraform Outputs
#  Project: PythonFlask DevSecOps Pipeline
# ─────────────────────────────────────────────────────────────────────────────

# ── VPC Outputs ───────────────────────────────────────────────────────────────
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

# ── EKS Outputs ───────────────────────────────────────────────────────────────
output "eks_cluster_name" {
  description = "Name of the EKS cluster"
  value       = aws_eks_cluster.main.name
}

output "eks_cluster_endpoint" {
  description = "Endpoint of the EKS cluster"
  value       = aws_eks_cluster.main.endpoint
}

output "eks_cluster_version" {
  description = "Kubernetes version of EKS cluster"
  value       = aws_eks_cluster.main.version
}

# ── ECR Outputs ───────────────────────────────────────────────────────────────
output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.flask_app.repository_url
}

# ── RDS Outputs ───────────────────────────────────────────────────────────────
output "rds_endpoint" {
  description = "Endpoint of the RDS MySQL instance"
  value       = aws_db_instance.mysql.endpoint
}

output "rds_db_name" {
  description = "Name of the MySQL database"
  value       = aws_db_instance.mysql.db_name
}

# ── kubectl Config Command ────────────────────────────────────────────────────
output "kubectl_config_command" {
  description = "Command to configure kubectl"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${aws_eks_cluster.main.name}"
}
