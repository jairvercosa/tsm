/* Executar Script para data acesso às receitas */
insert into acesso_usuario_receitas(usuario_id, receita_id)
select a.user_ptr_id as usuario_id , b.id as receita_id
  from acesso_usuario a, oportunidade_receita b;

/*Executar script para atualizar cadastro de clientes*/
update cliente_cliente
inner join oportunidade_oportunidade on cliente_cliente.id = oportunidade_oportunidade.cliente_id
set executivo_id = responsavel_id;