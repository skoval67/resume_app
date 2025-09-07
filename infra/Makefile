.PHONY: all

all: build_infra run_playbook

build_infra:
	@cd terraform;\
		terraform apply -auto-approve;\

run_playbook:
	@cd ansible; \
	    ansible-playbook -b playbook.yml
